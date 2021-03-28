from shorty.service import Shorty
import json
from configs.config import *


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


def test_choose_and_init_bitly():
    shorty_instance = Shorty(url="https://www.example.com", provider="bitly")
    shorty_instance._choose_and_init_provider()
    assert shorty_instance.header == {GeneralStrs.AUTHORIZATION: BitLy.TOKEN, GeneralStrs.CONTENT_TYPE: BitLy.CONTENT_TYPE}
    assert shorty_instance.URL_method == BitLy.API_URL


def test_choose_and_init_tinyurl():
    shorty_instance = Shorty(url="https://www.example.com",
                             provider="tinyurl")
    shorty_instance._choose_and_init_provider()
    assert shorty_instance.URL_method == TinyUrl.API_URL


def test_choose_and_init_unknown():
    shorty_instance = Shorty(url="https://www.example.com",
                             provider="dummyprovider")
    shorty_instance._choose_and_init_provider()
    assert shorty_instance.provider == GeneralStrs.UNKNOWN


def test_alter_provider():
    shorty_instance = Shorty(url="https://www.example.com")
    shorty_instance._alter_provider()
    assert shorty_instance.URL_method == TinyUrl.API_URL


def test_make_requests_unknown():
    shorty_instance = Shorty(url="https://www.example.com",
                             provider="dummyprovider")

    response = shorty_instance._make_requests()
    assert response.get_status_code() == 404
    assert response.get_message() == Messages.WRONG_PROVIDER_MSG


def test_make_requests_bitly(mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=200, url="https://www.example.com",
                                           text="https://bitly.com/peakb",
                                           provider="https://api-ssl.bitly.com/v4/shorten"))

    shorty_instance = Shorty(url="https://www.example.com",
                             provider="bitly")

    response = shorty_instance._make_requests()
    assert response.get_status_code() == 200
    assert response.get_url() == "https://www.example.com"
    assert response.get_link() == "https://bitly.com/peakb"
    assert response.get_provider() == "https://api-ssl.bitly.com/v4/shorten"


def test_make_requests_tinyurl(mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=200, url="https://example.com",
                                           text="https://tinyurl.com/peakb",
                                           provider="http://tinyurl.com/api-create.php"))

    shorty_instance = Shorty(url="https://www.example.com",
                             provider="tinyurl")

    response = shorty_instance._make_requests()
    assert response.get_status_code() == 200
    assert response.get_url() == "https://www.example.com"
    assert response.get_link() == "https://tinyurl.com/peakb"
    assert response.get_provider() == "http://tinyurl.com/api-create.php"


def test_shorten_success(mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=201, url="https://example.com",
                                           text="https://tinyurl.com/peakb",
                                           provider="http://tinyurl.com/api-create.php"))

    shorty_instance = Shorty(url="https://www.example.com",
                             provider="tinyurl")

    response = shorty_instance.shorten()

    assert response.json['url'] == "https://www.example.com"
    assert response.json['link'] == "https://tinyurl.com/peakb"


def test_shorten_fail(mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=400, url="https://example.com",
                                           text=None,
                                           provider="http://tinyurl.com/api-create.php"))

    shorty_instance = Shorty(url="https://www.example.com",
                             provider="tinyurl")

    response = shorty_instance.shorten()

    assert response.json['status_code'] == 400
    assert response.json['message'] == "Bad Request"


def test_shorten_fallback_fail(mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=400, url="https://example.com",
                                           text=None, provider=None))

    shorty_instance = Shorty(url="https://www.example.com")

    response = shorty_instance.shorten()

    assert response.json['status_code'] == 400
    assert response.json['message'] == "Bad Request"
