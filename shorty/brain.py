import re
from typing import Optional
from urllib.parse import urlencode
import requests
from shorty.errors import ErrorHandler
from flask import jsonify


class Shorty:

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
        else:
            self.provider = "unknown"

    def _alter_provider(self):
        self.provider = "tinyurl" if self.provider == "bitly" else "bitly"
        self._choose_and_init_provider()

    def _make_requests(self):

        if self.provider == "unknown":
            return {"status_code": 404,
                    "message": "Not supported Provider. Choose between bit.ly and tinyurl"}
        elif "tinyurl" in self.provider.lower():
            url = self.URL_method + "?" + urlencode({"url": self.params['long_url']})
            res = requests.post(url)
            return {"status_code": res.status_code, "url": self.params['long_url'],
                    "link": res.text,
                    "provider": self.URL_method}
        elif "bitly" in self.provider.lower():
            res = requests.post(self.URL_method, json=self.params, headers=self.header)
            link = None if res.status_code not in [200, 201] else res.json().get("link")
            return {"status_code": res.status_code, "url": self.params['long_url'],
                    "link": link, "provider": self.URL_method}

    def shorten(self, supplied_provider=False):
        if not supplied_provider:
            results = self._make_requests()
            if results['status_code'] not in [200, 201]:
                self._alter_provider()
                results = self._make_requests()
                if results['status_code'] not in [200, 201]:
                    return jsonify(ErrorHandler(status_code=results['status_code']).to_dict())
                else:
                    return jsonify(results)
            else:
                return jsonify(results)

        elif supplied_provider:
            results = self._make_requests()
            if results['status_code'] not in [200, 201]:
                message = results['message'] if "message" in results else None
                return jsonify(
                    ErrorHandler(message=message, status_code=results['status_code']).to_dict())
            else:
                return jsonify(results)

