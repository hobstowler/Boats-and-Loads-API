from functools import wraps
from flask import request
from google.auth.transport import requests
from google.oauth2 import id_token

client_id = '38857299416-r6gj2pdtsdhbk1cuskul5culi0g9ojvi.apps.googleusercontent.com'


# Verify the JWT in the request's Authorization header
# adapted from https://developers.google.com/identity/sign-in/web/backend-auth
def verify_jwt(request):
    try:
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization'].split()
            token = auth_header[1]
        else:
            return None
        payload = id_token.verify_oauth2_token(token, requests.Request(), client_id)
        return payload
    except ValueError:
        return None
    except Exception as e:
        return None


def require_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = verify_jwt(request)
        return func(payload)
    return wrapper


@require_jwt
def test_func(payload):
    print(payload)
