import json


class ResponseOverride(Exception):
    def __init__(self, status_code: int = None, url: str = None, link: str = None,
                 provider: str = None, message: str = None):
        self.status_code = status_code
        self.url = url
        self.text = link
        self.provider = provider
        self.message = message
        self.attributes = {"status_code": self.status_code, "url": self.url, "link": self.text,
                           "provider": self.provider, "message": self.message}
        self.attributes_str = json.dumps(self.attributes)

    def json(self):
        return json.loads(self.attributes_str)

    def to_dict(self):
        return {"status_code": self.status_code, "url": self.url, "link": self.text,
                "provider": self.provider, "message": self.message}
