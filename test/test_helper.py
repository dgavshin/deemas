import server

last_logged_message = ""


class MockCtxLog:
    def info(self, data):
        pass

    def debug(self, data):
        pass

    def warn(self, data):
        pass

    def error(self, data):
        global last_logged_message
        last_logged_message = data
        pass


server.ctx.log = MockCtxLog()
