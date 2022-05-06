from mitmproxy.tcp import TCPFlow, TCPMessage
from utils import log
from config import FLAG_FORMAT, FLAG_LEN, ALLOWABLE_FLAG_COUNT


def check(flow: TCPFlow) -> bool:
    """
    :param flow: поток http сообщения
    :return: Если True, флаги расшфируются, если False, то останутся зашифрованными
    """

    log.debug("[<rule_name>] Начало обработки TCP правила")
    # Последнее сообщение в потоке
    message: TCPMessage = flow.messages[-1]
    # Полезная нагрузка сообщения
    content: bytes = message.content
    # True, если это request, false если response
    from_client: bool = message.from_client

    decision = True
    log.debug(f"[<rule_name>] TCP правило вернуло {decision}")
    return decision
