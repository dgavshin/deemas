from mitmproxy import tcp

from crypto import encrypt_flags, decrypt_flags
from flaghandler import FlagHandler, contains_flag
from utils import log


class TCPFlagHandler(FlagHandler):

    def __init__(self):
        super().__init__()

    def tcp_message(self, flow: tcp.TCPFlow):
        message: tcp.TCPMessage = flow.messages[-1]
        content: bytes = message.content

        log.info(
            f"tcp_message[{message.from_client=}), "
            f"content = {content if len(content) < 20 else content[:20] + b'...'}]]")
        if not message.content or not contains_flag(message.content):
            log.debug("В пакете нет флагов, пакет пропускается")
            return flow

        # Если пакет от клиента, то используем функцию encrypt_flags, иначе decrypt_flags
        crypto_func, decision_func = (encrypt_flags, self.service.encrypt_decision) \
            if message.from_client else (decrypt_flags, self.service.decrypt_decision)

        decision = True
        error = False
        try:
            decision = decision_func(flow)
        except Exception as e:
            log.info(f"[{decision_func.__name__}] Некоторые проверки не смогли выполниться: " + str(e))

        if decision:
            if not error:
                log.info(f"[{decision_func.__name__}] Флаги будут расшифрованы, {decision=}")
            message.content = crypto_func(content, self.encryptor)
        else:
            log.info(f"[{decision_func.__name__}] Не все проверки были пройдены, {decision=}")
        return flow


addons = [
    TCPFlagHandler()
]
