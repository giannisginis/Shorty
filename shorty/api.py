from flask import Blueprint, jsonify, request
from shorty.service import Shorty
from shorty.errors import ErrorHandler
from shorty.validators import Validators

api = Blueprint('api', __name__)


@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    req = request.get_json()
    status_code, message = Validators(req).validate()
    if status_code != 200:
        return jsonify(
            ErrorHandler(message=message, status_code=status_code).to_dict())

    service = Shorty(url=req.get('url'), provider=req.get("provider"))
    return service.shorten()