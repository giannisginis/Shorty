"""
URL shorten with TinyURL and bit.ly API
"""
import traceback
from urllib.parse import urlencode
import requests


class UrlShortenTinyurl:
    URL_method = "http://tinyurl.com/api-create.php"

    def shorten(self, long_url):
        try:
            url = self.URL_method + "?" + urlencode({"url": long_url})
            res = requests.get(url)
            print(f'Shortening Method: {self.URL_method}')
            print("STATUS CODE:", res.status_code)
            print("   LONG URL:", long_url)
            print("  SHORT URL:", res.text)
        except Exception as e:
            raise


class UrlShortenBitly:
    header = {
        "Authorization": "Bearer 8ce4e9f7e73b0da7303a325b64bbb1c540e16a73",
        "Content-Type": "application/json"
    }
    URL_method = "https://api-ssl.bitly.com/v4/shorten"

    def __init__(self, long_url):
        self.params = {"long_url": long_url}

    def shorten(self):
        try:
            res = requests.post(self.URL_method, json=self.params, headers=self.header)
            print(f'Shortening Method: {self.URL_method}')
            print("STATUS CODE:", res.status_code)
            print("   LONG URL:", res.json().get("long_url"))
            print("  SHORT URL:", res.json().get("link"))
        except Exception as e:
            raise


if __name__ == '__main__':
    req = {"long_url": "https://mastoras.com",
           "url_link": "bit.ly"}

    if "tinyurl" in req["url_link"].lower():
        try:
            obj = UrlShortenTinyurl()
            obj.shorten(req["long_url"])
        except Exception as e:
            traceback.print_exc()
    elif "bit.ly" in req["url_link"].lower():
        try:
            obj = UrlShortenBitly(long_url=req["long_url"])
            re = obj.shorten()
        except Exception as e:
            traceback.print_exc()
    else:
        print("Wrong link method")
