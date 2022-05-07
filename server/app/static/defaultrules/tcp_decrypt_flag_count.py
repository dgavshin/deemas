import re

from mitmproxy.tcp import TCPFlow

from config import FLAG_FORMAT, ALLOWABLE_FLAG_COUNT


def check(flow: TCPFlow) -> bool:
    """
    :param flow: поток http сообщения
    :return: возращает True, если флагов в сообщении было меньше или равно, чем
             разрешенное количество, иначе False
    """
    return len(set(re.findall(FLAG_FORMAT, flow.messages[-1].content))) <= ALLOWABLE_FLAG_COUNT
