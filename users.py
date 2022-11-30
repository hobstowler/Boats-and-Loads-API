from flask import Blueprint, request, jsonify
from google.cloud import datastore
from verification import verify_jwt, require_jwt

client = datastore.Client()

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def users():
    if request.method == 'GET':
        if request.accept_mimetypes.accept_json:
            return get_all_users()
        else:
            return '', 406
    else:
        return '', 405


def get_all_users():
    query = client.query(kind='User')
    results = query.fetch()
    res = []
    for result in results:
        user = dict(result)
        user['id'] = result.id
        res.append(user)
    return jsonify(res), 200



