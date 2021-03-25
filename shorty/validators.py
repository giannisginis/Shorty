import validators
from configs.config import Messages


class Validators:
    def __init__(self, request):
        self.request = request

    @staticmethod
    def _validate_url_type(url):
        if not validators.url(url):
            status_code = 404
            message = Messages.WRONG_URL_MSG
        else:
            status_code = 200
            message = "OK"

        return status_code, message

    def _validate_request(self):
        if not self.request.get("url") or (
                len(self.request) == 2 and not self.request.get("provider")):
            status_code = 400
            message = Messages.WRONG_PARAMETER_MSG
        else:
            status_code = 200
            message = "OK"
        return status_code, message

    def validate(self):
        status_code, message = self._validate_request()
        if status_code == 200:
            status_code, message = self._validate_url_type(self.request.get("url"))

        return status_code, message
