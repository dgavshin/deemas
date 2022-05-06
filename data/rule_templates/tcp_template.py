from server import TCPFlow

"""
:param flow: поток tcp сообщения
:return: Если вернуть True, то флаги расшфируются, если False, то нет

         Пример - если в сообщении только 1 флаг, вернуть true, иначе false
         В случаес True у флагов есть шанс расшифроваться (если все остальные правила тоже True),
         во втором случае флаги точно не будут расшифровываться
"""


def check(flow: TCPFlow) -> bool:
    message = flow.messages[-1]
    content: bytes = message.content
    from_client: bool = message.from_client

    # Код здесь
    return True


if __name__ == "__main__":
    import os, sys
    SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    from flowmock import MockTCPFlow

    with_flag = MockTCPFlow(b"7769TY9X8G3KFDBP65TZU1B0653CFBA=", False)
    no_flag = MockTCPFlow(b"Just a text", True)
    print("Запуск правила с параметрами")
    print(f"Content with flag: {check(with_flag)}")
    print(f"Content without flag: {check(no_flag)}")

    # здесь пейлоад, чтоб потестить правило
    custom = MockTCPFlow(b"payload here", True)
    print(f"Custom: {check(custom)}")
