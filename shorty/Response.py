class Response(Exception):
    def __init__(self, status_code: int = None, url: str = None, link: str = None,
                 provider: str = None, message: str = None):
        self.status_code = status_code
        self.url = url
        self.link = link
        self.provider = provider
        self.message = message

    def to_dict(self):

        return {"status_code": self.status_code, "url": self.url, "link": self.link,
                "provider": self.provider, "message": self.message}
