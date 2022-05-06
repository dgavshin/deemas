from os import getenv

from dotenv import load_dotenv
from mitmproxy import ctx

from config import FLAG_LEN, FLAG_FORMAT, SERVICE_NAME_ENV, LOG_DIR
from crypto import get_encryptor, Encryptor
from dbmanager import get_service
from utils import log, configure_logging


def contains_flag(data: bytes) -> bool:
    if len(data) < FLAG_LEN:
        return False
    return FLAG_FORMAT.search(data)


class FlagHandler:
    """
    Этот класс перехватывает все входящие и исходящие сообщения
    и либо шифрует флаги в них, либо расшифровывает, в зависимости
    от их параметров и правил, загруженных при старте proxy.
    """

    def __init__(self):
        log.debug(f"Начало создания хендлера")

        load_dotenv()
        name = getenv(SERVICE_NAME_ENV)
        if name is None:
            log.error("Пустое значение переменной окружения SERVICE_NAME")
            ctx.master.shutdown()
            exit(1)

        configure_logging(LOG_DIR / f"{name}.logs")
        self.service = get_service(name)
        self.encryptor: Encryptor = get_encryptor()
        log.info(f"Создан handler для сервиса {self.service.name}")

        log.info(f"Количество condition правил: encrypt-%s, decrypt-%s"
                  % (len(self.service.encrypt_condition_rules),
                     len(self.service.decrypt_condition_rules)))
        log.info(f"Количество script правил: encrypt-%s, decrypt-%s"
                  % (len(self.service.encrypt_script_rules),
                     len(self.service.decrypt_script_rules)))
