from flask import Blueprint, jsonify, request
from schemas import UrlShortener
import traceback


api = Blueprint('api', __name__)


@api.route('/shortlinks', methods=['POST'])
def create_shortlink():

    results = dict()
    req = request.get_json()

    # shortenCode
    if not req.get("provider"):
        try:
            obj = UrlShortener(url=req.get('url'))
            results = obj.shorten()
        except Exception as e:
            traceback.print_exc()
        return jsonify(results)
    elif req.get("provider"):
        try:
            obj = UrlShortener(url=req.get('url'), provider=req.get("provider"))
            results = obj.shorten()
        except Exception as e:
            traceback.print_exc()
        return jsonify(results)

