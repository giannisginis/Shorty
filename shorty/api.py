from flask import Blueprint, jsonify, request
from schemas import UrlShortener
from shorty.errors import ErrorHandler

api = Blueprint('api', __name__)


@api.route('/shortlinks', methods=['POST'])
def create_shortlink():

    results = dict()
    req = request.get_json()
    if not req.get("url") or (len(req) == 2 and not req.get("provider")):
        return jsonify(
            ErrorHandler(
                'Invalid parameters. Provide a <url> and optionally a <provider> parameter.',
                status_code=400).to_dict())

    # shortenCode
    if not req.get("provider"):
        obj = UrlShortener(url=req.get('url'))
        results = obj.shorten()
        if results['status_code'] not in [200, 201]:
            return jsonify(ErrorHandler(status_code=results['status_code']).to_dict())
        else:
            return jsonify(results)

    elif req.get("provider"):
        obj = UrlShortener(url=req.get('url'), provider=req.get("provider"))
        results = obj.shorten()
        if results['status_code'] not in [200, 201]:
            message = results['message'] if "message" in results else None
            return jsonify(
                ErrorHandler(message=message, status_code=results['status_code']).to_dict())
        else:
            return jsonify(results)
