import re
from urllib.parse import unquote_to_bytes

from config import FLAG_FORMAT, ALLOWABLE_FLAG_COUNT
from mitmproxy.ctx import log
from mitmproxy.http import HTTPFlow


def check(flow: HTTPFlow) -> bool:
    """
    :param flow: поток http сообщения
    :return: возращает True, если флагов в сообщении было меньше или равно, чем
             разрешенное количество, иначе False
    """
    log.debug(f"[http decrypt rule] Выполнение проверки количества флагов в ответе сервера")
    flags = re.findall(FLAG_FORMAT, unquote_to_bytes(flow.response.content))
    res = len(set(flags)) <= ALLOWABLE_FLAG_COUNT
    log.debug(f"[http decrypt rule] Результат выполнения правила: {res}")
    return res
