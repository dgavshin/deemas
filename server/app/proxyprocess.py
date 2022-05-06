from subprocess import Popen, PIPE, STDOUT

from proxy.config import SERVICE_NAME_ENV
from server.app import app
from server.app.models import Protocol
from server.app.models import Service


class ProxyProcess(Popen):
    def __init__(self, service: Service, **kwargs):
        self.port = service.port
        proxy_args = kwargs.pop("process_args")
        app.logger.debug(f"Создание proxy процесса: {' '.join(proxy_args)}")
        super(ProxyProcess, self).__init__(args=proxy_args,
                                           env={SERVICE_NAME_ENV: service.name,
                                                "SYSTEMROOT": app.config.get("SYSTEM_ROOT")},
                                           stdout=PIPE,
                                           stderr=STDOUT)


class HTTPProxyProcess(ProxyProcess):
    def __init__(self, service: Service):
        if service.protocol is not Protocol.HTTP:
            raise ValueError(f"Неподдерживаемый протокол {service.protocol}, требуется Protocol.HTTP")

        http_proxy_args = [
            app.config["MITMDUMP_EXECUTABLE"],
            "-m", f"reverse:http://{service.proxy_host}:{service.proxy_port}",
            "-s", str(app.config["PROXY_ADDONS"]["http"]),
            "-p", str(service.port),
            "--set", "block_global=false",
            "--verbose"
        ]
        super(HTTPProxyProcess, self).__init__(service=service, process_args=http_proxy_args)


class TCPProxyProcess(ProxyProcess):
    def __init__(self, service: Service):
        if service.protocol is not Protocol.TCP:
            raise ValueError(f"Неподдерживаемый протокол {service.protocol}, требуется Protocol.TCP")

        tcp_proxy_args = [
            app.config["MITMDUMP_EXECUTABLE"],
            "-m", f"reverse:{service.proxy_host}:{service.proxy_port}",
            "-s", str(app.config["PROXY_ADDONS"]["tcp"]),
            "-p", str(service.port),
            "--rawtcp",
            "--tcp-hosts", ".*",
            "--set", "block_global=false",
            "--verbose"
        ]
        super(TCPProxyProcess, self).__init__(service=service, process_args=tcp_proxy_args)
