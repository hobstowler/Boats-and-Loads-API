from flask import Blueprint, request, jsonify
from google.cloud import datastore
from verification import verify_jwt, require_jwt

client = datastore.Client()

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=['GET'])
def users(payload):
    if request.method == 'GET':
        return get_all_users(request)
    elif request.method == 'POST' and request.is_json:
        pass
    else:
        return '', 406


@bp.route('/login', methods=['POST'])
def login():
    pass


@bp.route('/new', methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        if request.is_json:
            pass
        else:
            return '', 415
    elif request.method == 'GET':
        pass


def get_all_users():
    query = client.query(kind='User')
    results = query.fetch()
    res = []
    for result in results:
        user = dict(result)
        user['id'] = result.id
        res.append(user)
    return jsonify(res), 200



