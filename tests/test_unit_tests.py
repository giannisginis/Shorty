import json
from requests.exceptions import Timeout


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


def test_success_tinyrul(post, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=200, url="https://example.com",
                                       text="https://tinyurl.com/peakb",
                                       provider="http://tinyurl.com/api-create.php"))
    response = post('/shortlinks', data={'url': "https://example.com", 'provider': 'tinyurl'})
    assert response.json['link'] == "https://tinyurl.com/peakb"
    assert response.json['url'] == "https://example.com"


def test_fail_tinyurl(post, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=400))
    response = post('/shortlinks', data={'url': 'https://example.com', 'provider': 'tinyurl'})
    assert response.json['status_code'] == 400


def test_success_bitly(post, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=200, url="https://example.com",
                                       text="https://bit.ly/3cO2cpC",
                                       provider="https://api-ssl.bitly.com/v4/shorten"))
    response = post('/shortlinks', data={'url': 'https://example.com', 'provider': 'bitly'})
    assert response.json['link'] == "https://bit.ly/3cO2cpC"
    assert response.json['url'] == "https://example.com"


def test_fail_bitly(post, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=400))
    response = post('/shortlinks', data={'url': 'https://example.com', 'provider': 'bitly'})
    assert response.json['status_code'] == 400


def test_success_no_provider(post, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=200, url="https://example.com",
                                       text="https://bit.ly/3cO2cpC",
                                       provider="https://api-ssl.bitly.com/v4/shorten"))
    response = post('/shortlinks', data={'url': 'https://example.com'})
    assert response.json['link'] == "https://bit.ly/3cO2cpC"
    assert response.json['url'] == "https://example.com"


def test_fail_no_provider(post, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=MockResponse(status_code=400))
    response = post('/shortlinks', data={'url': 'https://example.com'})
    assert response.json['status_code'] == 400


def test_unknown_provider(post):
    response = post('/shortlinks', data={'url': 'https://example.com', "provider": "dummy"})
    assert response.json['status_code'] == 404
    assert response.json['message'] == "Not supported Provider. Choose between bit.ly and tinyurl"


def test_fail_request_params_url(post):
    response = post('/shortlinks', data={'ur': 'https://example.com', "provider": "dummy"})
    assert response.json['status_code'] == 400
    assert response.json['message'] == "Invalid parameters. Provide a <url> and optionally " \
                                       "a <provider> parameter."


def test_fail_request_params_provider(post):
    response = post('/shortlinks', data={'ur': 'https://example.com', "providr": "tinyurl"})
    assert response.json['status_code'] == 400
    assert response.json['message'] == "Invalid parameters. Provide a <url> and optionally " \
                                       "a <provider> parameter."


def test_fail_request_params_invalid_url(post):
    response = post('/shortlinks', data={'url': 'example.com', "provider": "tinyurl"})
    assert response.json['status_code'] == 404
    assert response.json['message'] == "Invalid Url. Please provide a valid url"


def test_timeout_tinyurl(post, mocker):
    mocker.patch('shorty.handler.requests.post', side_effect=Timeout)
    response = post('/shortlinks', data={'url': 'https://example.com', "provider": "tinyurl"})
    assert response.json['status_code'] == 408


def test_timeout_bitly(post, mocker):
    mocker.patch('shorty.handler.requests.post', side_effect=Timeout)
    response = post('/shortlinks', data={'url': 'https://example.com', "provider": "bitly"})
    assert response.json['status_code'] == 408
