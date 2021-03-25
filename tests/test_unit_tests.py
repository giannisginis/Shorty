import json


class Response:
    def __init__(self, status_code: int = None, url: str = None, text: str = None,
                 provider: str = None):
        self.status_code = status_code
        self.url = url
        self.text = text
        self.provider = provider
        self.attributes = {"url": self.url, "link": self.text}
        self.attributes_str = json.dumps(self.attributes)

    def json(self):
        return json.loads(self.attributes_str)


def test_success_tinyrul(get, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=Response(status_code=200, url="https://example.com",
                                       text="https://tinyurl.com/peakb",
                                       provider="http://tinyurl.com/api-create.php"))
    response = get('/shortlinks', data={'url': "https://example.com", 'provider': 'tinyurl'})
    assert response.json['status_code'] == 200
    assert response.json['link'] == "https://tinyurl.com/peakb"
    assert response.json['url'] == "https://example.com"


def test_fail_tinyurl(get, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=Response(status_code=400))
    response = get('/shortlinks', data={'url': 'https://example.com', 'provider': 'tinyurl'})
    assert response.json['status_code'] == 400


def test_success_bitly(get, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=Response(status_code=200, url="https://example.com",
                                       text="https://bit.ly/3cO2cpC",
                                       provider="https://api-ssl.bitly.com/v4/shorten"))
    response = get('/shortlinks', data={'url': 'https://example.com', 'provider': 'bitly'})
    assert response.json['status_code'] == 200
    assert response.json['link'] == "https://bit.ly/3cO2cpC"
    assert response.json['url'] == "https://example.com"


def test_fail_bitly(get, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=Response(status_code=400))
    response = get('/shortlinks', data={'url': 'https://example.com', 'provider': 'bitly'})
    assert response.json['status_code'] == 400


def test_success_no_provider(get, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=Response(status_code=200, url="https://example.com",
                                       text="https://bit.ly/3cO2cpC",
                                       provider="https://api-ssl.bitly.com/v4/shorten"))
    response = get('/shortlinks', data={'url': 'https://example.com'})
    assert response.json['status_code'] == 200
    assert response.json['link'] == "https://bit.ly/3cO2cpC"
    assert response.json['url'] == "https://example.com"


def test_fail_no_provider(get, mocker):
    mocker.patch('shorty.handler.requests.post',
                 return_value=Response(status_code=400))
    response = get('/shortlinks', data={'url': 'https://example.com'})
    assert response.json['status_code'] == 400


def test_unknown_provider(get):
    response = get('/shortlinks', data={'url': 'https://example.com', "provider": "dummy"})
    assert response.json['status_code'] == 404
    assert response.json['message'] == "Not supported Provider. Choose between bit.ly and tinyurl"


def test_fail_request_params_url(get):
    response = get('/shortlinks', data={'ur': 'https://example.com', "provider": "dummy"})
    assert response.json['status_code'] == 400
    assert response.json['message'] == "Invalid parameters. Provide a <url> and optionally " \
                                       "a <provider> parameter."


def test_fail_request_params_provider(get):
    response = get('/shortlinks', data={'ur': 'https://example.com', "providr": "tinyurl"})
    assert response.json['status_code'] == 400
    assert response.json['message'] == "Invalid parameters. Provide a <url> and optionally " \
                                       "a <provider> parameter."