from timeit import default_timer as timer

from httpaddon import HttpFlagHandler


class MockContent:
    def __init__(self, content: bytes):
        self.content = content


class MockHttpFlow:
    def __init__(self, data: bytes):
        self.request = MockContent(data)
        self.response = MockContent(data)


if __name__ == "__main__":

    repeat_num = 1000000
    flow = MockHttpFlow(b"1111111111111111111111111111111=")

    start = timer()
    handler = HttpFlagHandler()
    for i in range(repeat_num):
        handler.response(flow)
    end = timer()
    print(f"Request time: {end - start}s.")

    start = timer()
    handler = HttpFlagHandler()
    for i in range(repeat_num):
        handler.request(flow)
    end = timer()
    print(f"Request time: {end - start}s.")
