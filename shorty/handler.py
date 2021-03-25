import requests
from urllib.parse import urlencode
from typing import Dict, Any


class Handler:
    def __init__(self, api_provider: str = None, params: Dict[str, Any] = None,
                 headers: Dict[str, Any] = None):
        self.api_provider = api_provider
        self.parameters = params
        self.headers = headers

    def post_request(self, provider: str):
        if provider == "tinyurl":
            url = self.api_provider + "?" + urlencode({"url": self.parameters['long_url']})
            return requests.post(url)
        elif provider == "bitly":
            return requests.post(self.api_provider, json=self.parameters, headers=self.headers)
