from shorty.ResponseOverride import ResponseOverride

data = {"status_code": 200, "url": "https://www.example.com", "link": "https://tinyurl.com/cru6j",
        "provider": "tinyurl", "message": "OK"}


def test_ResponseOverride_get_methods():
    response = ResponseOverride(status_code=data["status_code"], url=data["url"], link=data["link"],
                     provider=data["provider"], message=data["message"])

    assert response.get_link() == "https://tinyurl.com/cru6j"
    assert response.get_status_code() == 200
    assert response.get_provider() == "tinyurl"
    assert response.get_message() == "OK"
    assert response.get_url() == "https://www.example.com"


def test_ResponseOverride_json_method():
    response_json = ResponseOverride(status_code=data["status_code"], url=data["url"], link=data["link"],
                                provider=data["provider"], message=data["message"]).json()

    assert response_json.get("status_code") == 200
    assert response_json.get("url") == "https://www.example.com"


def test_ResponseOverride_todict_method():
    response_dict = ResponseOverride(status_code=data["status_code"], url=data["url"], link=data["link"],
                                provider=data["provider"], message=data["message"]).to_dict()

    assert response_dict["link"] == "https://tinyurl.com/cru6j"
    assert response_dict["status_code"]== 200
    assert response_dict["provider"] == "tinyurl"
    assert response_dict["message"] == "OK"
    assert response_dict["url"] == "https://www.example.com"