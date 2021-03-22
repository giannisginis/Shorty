import re
from typing import Optional
from urllib.parse import urlencode
import requests


class UrlShortener:

    def __init__(self, url: str, provider: Optional[str] = None):
        self.provider = re.sub(r'[^\w\s]', '', provider) if provider is not None else "bitly"
        self.params = {"long_url": url}
        self._choose_and_init_provider()

    def _choose_and_init_provider(self):
        if "tinyurl" in self.provider.lower():
            self.URL_method = "http://tinyurl.com/api-create.php"
        elif "bitly" in self.provider.lower():
            self.header = {
                "Authorization": "Bearer 8ce4e9f7e73b0da7303a325b64bbb1c540e16a73",
                "Content-Type": "application/json"
            }
            self.URL_method = "https://api-ssl.bitly.com/v4/shorten"

    def shorten(self):

        if "tinyurl" in self.provider.lower():
            url = self.URL_method + "?" + urlencode({"url": self.params['long_url']})
            res = requests.get(url)
            return {"status_code": res.status_code, "url": self.params['long_url'],
                    "link": res.text,
                    "provider": self.URL_method}
        elif "bitly" in self.provider.lower():
            res = requests.post(self.URL_method, json=self.params, headers=self.header)
            return {"status_code": res.status_code, "url": self.params['long_url'],
                    "link": res.json().get("link"), "provider": self.URL_method}
        else:
            return {"status_code": 400, "url": self.params["long_url"], "link": None,
                    "provider": "Not supported Provider. Choose between bit.ly and tinyurl"}
