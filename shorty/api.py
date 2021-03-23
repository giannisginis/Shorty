from flask import Blueprint, jsonify, request
from shorty.brain import Shorty
from shorty.errors import ErrorHandler

api = Blueprint('api', __name__)


@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    req = request.get_json()
    if not req.get("url") or (len(req) == 2 and not req.get("provider")):
        return jsonify(
            ErrorHandler(
                'Invalid parameters. Provide a <url> and optionally a <provider> parameter.',
                status_code=400).to_dict())

    if not req.get("provider"):
        obj = Shorty(url=req.get('url'))
        return obj.shorten(supplied_provider=False)
    elif req.get("provider"):
        obj = Shorty(url=req.get('url'), provider=req.get("provider"))
        return obj.shorten(supplied_provider=True)