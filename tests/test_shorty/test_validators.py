from shorty.validators import Validators
import json
from configs.config import *


def dict2json(file):
    return json.loads(json.dumps(file))


def test_url_validation_success():
    status_code, message = Validators(
        request=dict2json({"url": "https://www.example.com"}))._validate_url_type(
        "https://www.example.com")
    assert status_code == 200
    assert message == "OK"


def test_url_validation_fail():
    status_code, message = Validators(
        request=dict2json({"url": "//www.example.com"}))._validate_url_type(
        "www.example.com")

    assert status_code == 404
    assert message == Messages.WRONG_URL_MSG


def test_request_validation_only_url_success():
    status_code, message = Validators(
        request=dict2json({"url": "//www.example.com"}))._validate_request()

    assert status_code == 200
    assert message == "OK"


def test_request_validation_only_url_fail():
    status_code, message = Validators(
        request=dict2json({"ur": "//www.example.com"}))._validate_request()
    assert status_code == 400
    assert message == Messages.WRONG_PARAMETER_MSG


def test_request_validation_only_provider_success():
    status_code, message = Validators(
        request=dict2json({"url": "//www.example.com", "provider": "bitly"}))._validate_request()

    assert status_code == 200
    assert message == "OK"


def test_request_validation_provider_fail():
    status_code, message = Validators(
        request=dict2json({"url": "//www.example.com", "provier": "bitly"}))._validate_request()
    assert status_code == 400
    assert message == Messages.WRONG_PARAMETER_MSG


def test_request_end2end():
    status_code, message = Validators(
        request=dict2json({"url": "//www.example.com", "provier": "bitly"})).validate()
    assert status_code == 400
    assert message == Messages.WRONG_PARAMETER_MSG