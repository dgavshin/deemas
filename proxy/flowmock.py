class MockHTTPMessage:
    def __init__(self, content: bytes):
        self.content = content
        self.status_code = 200


class MockHTTPFlow:
    def __init__(self, data: bytes):
        self.request = MockHTTPMessage(data)
        self.response = MockHTTPMessage(data)


class MockTCPMessage:
    def __init__(self, content: bytes, from_client: bool):
        self.content = content
        self.from_client = from_client


class MockTCPFlow:
    def __init__(self, content: bytes, from_client: bool):
        self.messages = [MockTCPMessage(content, from_client)]
