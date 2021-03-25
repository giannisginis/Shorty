from flask import Blueprint, jsonify, request
from shorty.brain import Shorty
from shorty.errors import ErrorHandler
from shorty.validators import Validators

api = Blueprint('api', __name__)


@api.route('/shortlinks', methods=['GET'])
def create_shortlink():
    req = request.get_json()
    status_code, message = Validators(req).validate()
    if status_code != 200:
        return jsonify(
            ErrorHandler(message=message, status_code=status_code).to_dict())

    if not req.get("provider"):
        obj = Shorty(url=req.get('url'))
        return obj.shorten(supplied_provider=False)
    elif req.get("provider"):
        obj = Shorty(url=req.get('url'), provider=req.get("provider"))
        return obj.shorten(supplied_provider=True)