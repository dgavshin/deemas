from urllib.parse import unquote_to_bytes

from mitmproxy.http import HTTPFlow

from crypto import encrypt_flags, decrypt_flags
from flaghandler import FlagHandler, contains_flag
from utils import log


class HttpFlagHandler(FlagHandler):
    """
    Этот класс перехватывает все входящие и исходящие http сообщения
    и либо шифрует флаги в них, либо расшифровывает, в зависимости
    от их параметров.
    """

    def __init__(self):
        super().__init__()

    def request(self, flow: HTTPFlow) -> None:
        """
        Перехватывает входящие http пакеты и подменяет
        в них тело запроса. Все флаги, определенные форматом
        в конфигурации, будут зашифрованы и переданы далее
        серверу

        :param flow: поток входящего запроса
        """
        content: bytes = unquote_to_bytes(flow.request.content)
        log.info(f"[HttpFlagHandler.request] Перехвачен запрос")
        if not contains_flag(content):
            log.info("[HttpFlagHandler.request] В запросе нет флагов, пакет пропускается")
            return

        decision = True
        error = False
        try:
            decision = self.service.encrypt_decision(flow)
        except Exception as e:
            log.error("Некоторые проверки не смогли выполниться, флаги зашифровываются: " + str(e))

        if decision:
            if not error:
                log.info("[HttpFlagHandler.request] Флаги будут зашифрованы")
            flow.request.content = encrypt_flags(content, self.encryptor)
        else:
            log.info("[HttpFlagHandler.request] Не все проверки были пройдены, поэтому флаги не будут зашифрованы")

    def response(self, flow: HTTPFlow) -> None:
        """
        Перехватывает исходящие http пакеты и подменяет
        в них тело ответа. Все флаги, определенные форматом
        в конфигурации, будут расшифрованы и переданы далее
        клиенту

        :param flow: поток исходящего запроса
        """
        log.info(f"[HttpFlagHandler.response] Перехвачен ответ")
        content: bytes = unquote_to_bytes(flow.response.content)
        if content is None or not contains_flag(content):
            log.info("[HttpFlagHandler.response] В ответе нет флагов, пакет пропускается")
            return

        decision = True
        error = False

        try:
            decision = self.service.decrypt_decision(flow)
        except Exception as e:
            log.error("[HttpFlagHandler.response] Некоторые проверки не смогли выполниться,"
                     " флаги расшифровываются: " + str(e))

        if decision:
            if not error:
                log.info("[HttpFlagHandler.response] Флаги будут расшифрованы")
            flow.response.content = decrypt_flags(content, self.encryptor)
        else:
            log.info("Не все проверки были пройдены, флаги не будут расшифровываться")


addons = [
    HttpFlagHandler()
]
