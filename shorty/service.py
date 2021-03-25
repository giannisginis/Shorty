import re
from typing import Optional
from flask import jsonify
from shorty.ResponseOverride import ResponseOverride
from shorty.errors import ErrorHandler
from shorty.handler import Handler
from configs.config import *


class Shorty:

    def __init__(self, url: str, provider: Optional[str] = None):
        self.provider = re.sub(r'[^\w\s]', '', provider) if provider is not None else BitLy.NAME
        self.supplied_provider = False if not provider else True
        self.params = {"long_url": url}
        self.URL_method = None
        self.header = {}
        self._choose_and_init_provider()
        self.handler = Handler(api_provider=self.URL_method, params=self.params,
                               headers=self.header)

    def _choose_and_init_provider(self):
        if TinyUrl.NAME in self.provider.lower():
            self.URL_method = TinyUrl.API_URL
        elif BitLy.NAME in self.provider.lower():
            self.header = {
                GeneralStrs.AUTHORIZATION: BitLy.TOKEN,
                GeneralStrs.CONTENT_TYPE: BitLy.CONTENT_TYPE
            }
            self.URL_method = BitLy.API_URL
        else:
            self.provider = GeneralStrs.UNKNOWN

    def _alter_provider(self):
        self.provider = TinyUrl.NAME if self.provider == BitLy.NAME else BitLy.NAME
        self._choose_and_init_provider()
        self.handler = Handler(api_provider=self.URL_method, params=self.params,
                               headers=self.header)

    def _make_requests(self):

        if self.provider == GeneralStrs.UNKNOWN:
            return ResponseOverride(status_code=404, message=Messages.WRONG_PROVIDER_MSG)
        elif TinyUrl.NAME in self.provider.lower():
            res = self.handler.post_request(provider=self.provider)
            return ResponseOverride(status_code=res.status_code, url=self.params['long_url'], link=res.text,
                                    provider=self.URL_method)
        elif BitLy.NAME in self.provider.lower():
            res = self.handler.post_request(provider=self.provider)
            link = None if res.status_code not in [200, 201] else res.json().get("link")

            return ResponseOverride(status_code=res.status_code, url=self.params['long_url'], link=link,
                                    provider=self.URL_method)

    def shorten(self):
        if not self.supplied_provider:
            results = self._make_requests()
            if results.get_status_code() not in [200, 201]:
                self._alter_provider()
                results = self._make_requests()
                if results.get_status_code() not in [200, 201]:
                    return jsonify(ErrorHandler(status_code=results.get_status_code()).to_dict())
                else:
                    return jsonify({"url": results.get_url(), "link": results.get_link()})
            else:
                return jsonify({"url": results.get_url(), "link": results.get_link()})

        elif self.supplied_provider:
            results = self._make_requests()
            if results.get_status_code() not in [200, 201]:
                return jsonify(
                    ErrorHandler(message=results.get_message(),
                                 status_code=results.get_status_code()).to_dict())
            else:
                return jsonify({"url": results.get_url(), "link": results.get_link()})
