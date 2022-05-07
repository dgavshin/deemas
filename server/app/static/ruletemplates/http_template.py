from mitmproxy.http import HTTPFlow
from mitmproxy.ctx import log
from config import FLAG_FORMAT, FLAG_LEN, ALLOWABLE_FLAG_COUNT


def check(flow: HTTPFlow) -> bool:
    """
    :param flow: поток http сообщения
    :return: Если True, флаги расшфируются, если False, то останутся зашифрованными

             Некоторые полезные переменные:
             1. flow.[request/response].[content/headers/status_code]
             2. config.FLAG_FORMAT.find_all( ... <- подавать только байты)
             flow.*.content это bytes
    """

    log.debug("[<rule_name>] Начало выполнения HTTP правила <rule_name>")
    request: bytes = flow.request.content
    response: bytes = flow.response.content
    code: int = flow.response.status_code
    url: str = flow.request.url

    decision = True
    # Код здесь
    log.debug(f"[<rule_name>] HTTP правило вернуло {decision}")
    return decision

