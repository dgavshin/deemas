from server import HTTPFlow
"""
:param flow: поток http сообщения
:return: Если вернуть True, то флаги расшфируются, если False, то нет

         Пример - если в сообщении только 1 флаг, вернуть true, иначе false
         В случаес True у флагов есть шанс расшифроваться (если все остальные правила тоже True),
         во втором случае флаги точно не будут расшифровываться

         Некоторые полезные переменные:
         1. flow.[request/response].[content/headers/status_code]

         2. config.FLAG_FORMAT.find_all( ... <- подавать только байты) 

         flow.*.content это bytes
"""


def check(flow: HTTPFlow) -> bool:
    reqs: bytes = flow.request.content
    resp: bytes = flow.response.content
    status_code: int = flow.response.status_code

    # Код здесь
    return True


if __name__ == "__main__":
    import os, sys
    SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    from flowmock import MockHTTPFlow

    with_flag = MockHTTPFlow(b"7769TY9X8G3KFDBP65TZU1B0653CFBA=")
    no_flag = MockHTTPFlow(b"Just a text")
    print("Запуск правила с параметрами")
    print(f"Content with flag: {check(with_flag)}")
    print(f"Content without flag: {check(no_flag)}")

    # здесь пейлоад, чтоб потестить правило
    custom = MockHTTPFlow(b"payload here")
    print(f"Custom: {check(custom)}")

