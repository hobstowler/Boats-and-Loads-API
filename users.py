from flask import Blueprint, request, jsonify
from google.cloud import datastore
from verification import verify_jwt

client = datastore.Client()

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        payload = verify_jwt()
        if payload is None:
            return get_all_users(request)
        else:
            pass
    elif request.method == 'POST' and request.is_json:
        pass
    else:
        return '', 406


@bp.route('/login', methods=['POST'])
def login():
    pass


@bp.route('/new', methods=['GET','POST'])
def register_user(request):
    if request.method == 'POST':
        if request.is_json:
            pass
        else:
            return '', 415
    elif request.method == 'GET':
        pass


def get_all_users(request):
    pass


