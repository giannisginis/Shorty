import requests
from urllib.parse import urlencode
from typing import Dict, Any
from shorty.ResponseOverride import ResponseOverride
from configs.config import *


class Handler:
    def __init__(self, api_provider: str = None, params: Dict[str, Any] = None,
                 headers: Dict[str, Any] = None):
        self.api_provider = api_provider
        self.parameters = params
        self.headers = headers

    def post_request(self, provider: str):
        if provider == TinyUrl.NAME:
            try:
                url = self.api_provider + "?" + urlencode({"url": self.parameters['long_url']})
                return requests.post(url)
            except requests.exceptions.Timeout:
                return ResponseOverride(status_code=408)
        elif provider == BitLy.NAME:
            try:
                return requests.post(self.api_provider, json=self.parameters, headers=self.headers)
            except requests.exceptions.Timeout:
                return ResponseOverride(status_code=408)
