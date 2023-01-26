class FeedException(Exception):

    def __init__(self, message: str, url: str, code: int = 500):
        self.code = code
        self.message = message
        self.url = url
