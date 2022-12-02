from functools import wraps
from flask import request
from google.auth.transport import requests
from google.oauth2 import id_token

client_id = '919311581908-6gos83n2k2e6nd81emjd3qf77171od82.apps.googleusercontent.com'


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


def decode_jwt(token):
    try:
        return id_token.verify_oauth2_token(token, requests.Request(), client_id)
    except ValueError:
        return None
    except Exception:
        return None


def require_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = verify_jwt(request)
        return func(*args, **kwargs, payload=payload)
    return wrapper
