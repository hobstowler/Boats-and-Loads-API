import random
import flask
import requests as req
from flask import Flask, request, jsonify
from google.auth.transport import requests
from google.cloud import datastore
from google.cloud import secretmanager
from google.oauth2 import id_token
import boats
import loads
import users

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(boats.bp)
app.register_blueprint(users.bp)
app.register_blueprint(loads.bp)


client = datastore.Client()

client_id = '919311581908-6gos83n2k2e6nd81emjd3qf77171od82.apps.googleusercontent.com'
project_id = '919311581908'
secret_id = 'oauth'
secret_client = secretmanager.SecretManagerServiceClient()
secret_name = f'projects/{project_id}/secrets/{secret_id}/versions/latest'
response = secret_client.access_secret_version(request={"name": secret_name})
secret = response.payload.data.decode("UTF-8")


@app.route('/', methods=['GET'])
def index():
    start_url = f'{request.base_url}oauth'
    return f'<h1>Welcome!</h1>' \
           f'<p><a href={start_url}>Authenticate</a> with Google to generate a JWT. ' \
           f'If this is your first time logging in, an account will be created for you.</p>', 200


@app.route('/oauth', methods=['GET'])
def o_auth():
    # make state random by combining a random number with a random char sequence
    state = str(random.randint(0, 999999))
    for _ in range(10):
        state += chr(random.randint(65, 122))

    # store state in datastore for later
    new_state = datastore.Entity(client.key("State"))
    new_state.update({
        "value": state
    })
    client.put(new_state)

    auth_url = f'https://accounts.google.com/o/oauth2/v2/auth' \
               f'?response_type=code' \
               f'&client_id={client_id}' \
               f'&redirect_uri={request.host_url}returnauth' \
               f'&scope=profile' \
               f'&state={state}'

    return flask.redirect(auth_url)


@app.route('/returnauth', methods=['GET'])
def return_auth():
    query = client.query(kind="State")
    results = query.fetch()
    states = [result['value'] for result in list(results)]

    # check state against list of states in datastore.
    # TODO improve this...
    code = request.args.get('code')
    state = request.args.get('state')
    if state in states:
        json = {
            "code": code,
            "client_id": client_id,
            "client_secret": secret,
            "redirect_uri": f'{request.host_url}returnauth',
            "grant_type": "authorization_code"
        }
        res = req.post('https://oauth2.googleapis.com/token', json=json)
        if res.status_code == 200:
            res_json = res.json()
            id_token = res_json["id_token"]
            given_name = res_json["names"]["givenName"]
            family_name = res_json["names"]["familyName"]
            sub = register_new_user(id_token, given_name, family_name)  # assume JWT is always valid here.
            return flask.redirect(f'{request.host_url}userInfo'
                                  f'?jwt={id_token}'
                                  f'&sub={sub}'
                                  f'&givenName={given_name}'
                                  f'&familyName={family_name}')
        else:
            return 'bad response. could not get token'
    else:
        return 'Invalid state returned.', 401


def register_new_user(jwt, name, last_name) -> str:
    payload = id_token.verify_oauth2_token(jwt, requests.Request(), client_id)
    if payload is None:
        return
    query = client.query(kind='User')
    query.add_filter("sub", "=", payload['sub'])
    results = query.fetch(limit=1)
    if results is None:
        user = datastore.Entity(client.key('User"'))
        user.update({
            'given_name': name,
            'last_name': last_name,
            'sub': payload['sub']
        })
        client.put(user)
    return payload['sub']



@app.route('/userInfo')
def user_info():
    given_name = request.args.get('givenName')
    family_name = request.args.get('familyName')
    sub = request.args.get('sub')
    jwt = request.args.get('jwt')

    return f'<h1>Given Name</h1><p>{given_name}</p>' \
           f'<h1>Family Name</h1><p>{family_name}</p>' \
           f'<h1>sub</h1><p>{sub}</p>' \
           f'<h1>JWT Token</h1><p>{jwt}</p>'


# Decode the JWT supplied in the Authorization header
# adapted from https://developers.google.com/identity/sign-in/web/backend-auth
@app.route('/decode', methods=['GET'])
def decode_jwt():
    try:
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization'].split()
            token = auth_header[1]
        else:
            return jsonify({'Error': 'No Authorization in Request Header.'}), 401
        payload = id_token.verify_oauth2_token(token, requests.Request(), client_id)
        return payload
    except ValueError:
        return jsonify({'Error': 'Invalid token.'}), 401
    except:
        return jsonify({'Error': 'Invalid token or server error.'}), 401


if __name__ == '__main__':
    app.run()