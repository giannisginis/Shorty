import json
from requests.exceptions import Timeout
from configs.config import *
from shorty.handler import Handler


class MockResponse:
    def __init__(self, status_code: int = None, url: str = None, text: str = None,
                 provider: str = None, message: str = None):
        self.status_code = status_code
        self.url = url
        self.text = text
        self.provider = provider
        self.message = message
        self.attributes = {"url": self.url, "link": self.text, "message": self.message}
        self.attributes_str = json.dumps(self.attributes)

    def json(self):
        return json.loads(self.attributes_str)


def test_handler_bitly(mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=200, url="https://example.com",
                                           text="https://bitly.com/peakb",
                                           provider=BitLy.API_URL))

    response = Handler(api_provider=BitLy.API_URL, params={"long_url": "https://www.example.com"},
                       headers={GeneralStrs.AUTHORIZATION: BitLy.TOKEN,
                                GeneralStrs.CONTENT_TYPE: BitLy.CONTENT_TYPE}).post_request(
        provider=BitLy.NAME)

    assert response.json().get("link") == "https://bitly.com/peakb"
    assert response.status_code == 200


def test_handler_bitly_timeout(mocker):
    mocker.patch('shorty.handler.requests.post', side_effect=Timeout)

    response = Handler(api_provider=BitLy.API_URL, params={"long_url": "https://www.example.com"},
                       headers={GeneralStrs.AUTHORIZATION: BitLy.TOKEN,
                                GeneralStrs.CONTENT_TYPE: BitLy.CONTENT_TYPE}).post_request(
        provider=BitLy.NAME)

    assert response.status_code == 408


def test_handler_tinyurl(mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=200, url="https://example.com",
                                           text="https://tinyurl.com/peakb",
                                           provider=TinyUrl.API_URL))

    response = Handler(api_provider=TinyUrl.API_URL,
                       params={"long_url": "https://www.example.com"}).post_request(
        provider=TinyUrl.NAME)

    assert response.json().get("link") == "https://tinyurl.com/peakb"
    assert response.status_code == 200


def test_handler_tinyurl_timeout(mocker):
    mocker.patch('shorty.handler.requests.post', side_effect=Timeout)

    response = Handler(api_provider=TinyUrl.API_URL,
                       params={"long_url": "https://www.example.com"}).post_request(
        provider=TinyUrl.NAME)

    assert response.status_code == 408
