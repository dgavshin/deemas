import socket
import time
from pathlib import Path
from subprocess import TimeoutExpired
from typing import Dict, List
from typing import Type

from server.app import app, db
from server.app import scheduler
from server.app.proxyprocess import *

# Потокобезопасный "кэш" для активных прокси-процессов
proxy_processes: Dict[str, ProxyProcess] = {}

# Словарь с поддерживаемыми для создания прокси протоколами
proxy_protocols: Dict[Protocol, Type[ProxyProcess]] = {
    Protocol.HTTP: HTTPProxyProcess,
    Protocol.TCP: TCPProxyProcess
}
# Допустимое время для запуска прокси
WORK_APPROVE_TIMEOUT = 2


def is_proxy_enabled(service: Service):
    process: ProxyProcess = proxy_processes.get(service.name)
    if process is not None and process.returncode is None:
        return is_port_in_use(service.port)
    return False


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


def start_proxy(service: Service) -> None:
    """
    Создает proxy процесс, заносит в БД соответствующую запись,
    и обновляет локальный список запущенных процессов

    @param service сервис, для которого нужно запустить proxy
    """

    if is_proxy_enabled(service):
        raise ChildProcessError(f"Не удалось запустить proxy для сервиса {service.name}, процесс уже создан")

    if service.protocol not in proxy_protocols.keys():
        raise ValueError(f"Создание прокси для протокола {service.protocol} не поддерживается")

    if is_port_in_use(service.port):
        raise ValueError(f"Порт {service.port} уже занят другим процессом")

    process = proxy_protocols.get(service.protocol)(service)
    try:
        out, err = process.communicate(timeout=WORK_APPROVE_TIMEOUT)
        if process.returncode is not None:
            raise ChildProcessError("Не удалось запустить процесс mitmdump: out: %s, err: %s" % (out, err))
    except TimeoutExpired:
        pass

    proxy_processes.update({service.name: process})
    db.session.query(Service). \
        filter(Service.name == service.name). \
        update({"proxy_enabled": True})
    db.session.commit()
    app.logger.info(f"Прокси для сервиса {service.name} успешно запущен")


def stop_proxy(service: Service, db_record=True) -> None:
    """
    @param service сервис, для которого нужно запустить proxy
    @param db_record если True, изменяет поле service.proxy_enabled в False
    """

    try:
        process: ProxyProcess = proxy_processes.get(service.name)
        if process:
            process.kill()
    except (PermissionError, ValueError, KeyError) as e:
        app.logger.debug(f"Не удалось завершить процесс proxy сервиса {service.name}", e)

    if db_record:
        db.session.query(Service). \
            filter(Service.name == service.name). \
            update({"proxy_enabled": False})
    service_log: Path = app.config["LOG_DIR"] / (service.name + ".log")
    service_log.unlink(missing_ok=True)
    db.session.commit()
    app.logger.debug(f"Все операции по завершению прокси для сервиса {service.name} выполнены")


def restart_proxy(service: Service) -> None:
    stop_proxy(service, db_record=False)
    time.sleep(0.5)
    start_proxy(service)


@scheduler.task('interval', id='update_state', seconds=20)
def update_state() -> None:
    try:
        services: List["Service"] = db.session.query(Service).all()
        updates_services = []
        for service in services:
            try:
                if not is_proxy_enabled(service) and service.proxy_enabled is True:
                    stop_proxy(service, db_record=True)
                    updates_services.append(service.name)
            except ChildProcessError as e:
                app.logger.debug(f"Не удалось обновить статус сервиса {service.name}", e)
        if updates_services:
            app.logger.debug(f"Обновлен статус следующих сервисов: {updates_services}")
    except Exception as e:
        app.logger.debug("Не удалось выполнить обновление статусов proxy" + str(e))
