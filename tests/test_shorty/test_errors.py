from shorty.errors import ErrorHandler
from configs.config import *


def test_error_reporting_provided_attributes():
    data = {"message": Messages.WRONG_PROVIDER_MSG, "status_code": 404}
    error_report = ErrorHandler(message=data['message'], status_code=data["status_code"]).to_dict()

    assert error_report["status_code"] == 404
    assert error_report["message"] == "Not supported Provider. Choose between bit.ly and tinyurl"


def test_error_reporting_no_attributes():
    error_report = ErrorHandler().to_dict()

    assert error_report["status_code"] == 400
    assert error_report["message"] == "Bad Request"


def test_error_reporting_only_code_supplied():
    error_report = ErrorHandler(status_code=500).to_dict()

    assert error_report["status_code"] == 500
    assert error_report["message"] == "Internal Server Error"