from werkzeug.exceptions import HTTPException, RequestTimeout
from flask import Blueprint, jsonify
from http.client import responses
import requests

errors = Blueprint("errors", __name__)


class ErrorHandler(Exception):
    status_code = 400

    def __init__(self, message: str = None, status_code: int = None):
        if status_code is not None:
            self.status_code = status_code
        self.message = message if message else responses[self.status_code]

    def to_dict(self):
        rv = dict()
        rv['status_code'] = self.status_code
        rv['message'] = self.message

        return rv

