import flask
from flask import Blueprint, request, jsonify
from google.cloud import datastore

from verification import require_jwt

client = datastore.Client()

bp = Blueprint('boats', __name__, url_prefix='/boats')


@bp.route('/', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@require_jwt
def boats(payload):
    if payload is None:
        return jsonify({'error': 'JWT missing, expired, or invalid'}), 401

    if not request.accept_mimetypes.accept_json:
        return '', 406

    sub = payload['sub']
    if request.method == 'GET':  # get all boats
        return get_boats(sub)
    elif request.method == 'POST':  # create a boat
        if not request.is_json:
            return '', 415
        return create_boat(request, sub)
    else:
        return '', 405


def get_boats(sub):
    query = client.query(kind="Boat")
    query.add_filter('captain_id', '=', sub)
    total = len(list(query.fetch()))
    limit = int(request.args.get('limit', '5'))
    offset = int(request.args.get('offset', '0'))
    l_iterator = query.fetch(limit=limit, offset=offset)
    pages = l_iterator.pages
    boats = list(next(pages))
    if l_iterator.next_page_token:
        new_offset = offset + limit
        next_url = f'{request.base_url}?limit={limit}&offset={new_offset}'
    else:
        next_url = None

    results = []
    for boat in boats:
        res = dict(boat)
        res['id'] = boat.id
        res['self'] = f'{request.base_url}{boat.id}'
        if 'loads' in boat.keys():
            for load in boat['loads']:
                load['self'] = f'{request.host_url}loads/{load["id"]}'
        results.append(res)
    output = {
        "next": next_url,
        "total": total,
        "boats": results
    }
    return jsonify(output), 200


def create_boat(request: flask.Request, sub):
    json = request.get_json()
    try:
        name = json['name']
        boat_type = json['type']
        length = json['length']
        try:
            length = int(length)
        except ValueError:
            return jsonify({'error': 'Length must be an integer.'}), 400
    except KeyError as e:
        return jsonify({'Error': "The request object is missing at least one of the required attributes"}), 400
    else:
        boat = datastore.Entity(client.key("Boat"))
        boat.update({
            'name': name,
            'captain_id': sub,
            'type': boat_type,
            'length': length,
            'loads': []
        })
        client.put(boat)
        res = dict(boat)
        res['id'] = boat.id
        res['self'] = f'{request.base_url}{boat.id}'
        return jsonify(res), 201


@bp.route('/<boat_id>', methods=['GET', 'DELETE', 'PUT', 'PATCH'])
@require_jwt
def boat(boat_id: str, payload):
    if payload is None:
        return '', 401

    key = client.key('Boat', int(boat_id))
    boat = client.get(key)

    # if boat does not exist, then return 404
    if not boat:
        return jsonify({"Error": "No boat with this boat_id exists."}), 404

    sub = payload['sub']
    if not is_owner(boat, sub):
        return jsonify({"error": "The boat with this boat id is owned by another captain."}), 403

    if request.method == 'GET':  # get an existing boat
        if not request.accept_mimetypes.accept_json:
            return '', 406
        return get_boat(request, boat)

    elif request.method == 'DELETE':  # delete an existing boat and delete any loads
        return delete_boat(key, boat)

    elif request.method in ['PUT', 'PATCH']:
        if not request.is_json:
            return '', 415
        if not request.accept_mimetypes.accept_json:
            return '', 406

        if request.method == 'PUT':  # edit an existing boat
            return edit_boat(boat, request)
        elif request.method == 'PATCH':  # patch an existing boat
            return patch_boat(boat, request)


def get_boat(request, boat):
    res = dict(boat)
    res['id'] = boat.id
    res['self'] = f'{request.base_url}'
    res['loads'] = []
    for load in boat['loads']:
        res['loads'].append({
            "id": load['id'],
            "self": f'{request.host_url}loads/{load["id"]}'
        })
    return jsonify(res), 200


def edit_boat(boat, request):
    json = request.json
    try:
        name = json['name']
        boat_type = json['type']
        length = json['length']
        try:
            length = int(length)
        except ValueError:
            return jsonify({'error': 'Length must be an integer.'}), 400
    except KeyError as e:
        return jsonify({'Error': "The request object is missing at least one of the required attributes"}), 400
    else:
        boat['name'] = name
        boat['type'] = boat_type
        boat['length'] = length
        client.put(boat)

        res = dict(boat)
        res['id'] = boat.id
        res['self'] = f'{request.base_url}{boat.id}'

        return jsonify(res), 200


def patch_boat(boat, request):
    json = request.json
    name = json['name'] if 'name' in json else None
    boat_type = json['type'] if 'type' in json else None
    if 'length' in json:
        try:
            length = int(json['length'])
        except ValueError:
            return jsonify({'error': 'Length must be an integer.'}), 400
    else:
        length = None

    boat['name'] = name if name else boat['name']
    boat['type'] = boat_type if boat_type else boat['type']
    boat['length'] = length if length else boat['length']
    client.put(boat)

    res = dict(boat)
    res['id'] = boat.id
    res['self'] = f'{request.base_url}{boat.id}'

    return jsonify(res), 200


def delete_boat(key, boat):
    query = client.query(kind='Load')
    query.add_filter("carrier.id", "=", boat.id)
    loads = query.fetch()
    for load in loads:
        load['carrier'] = None
        client.put(load)

    client.delete(key)
    return '', 204


@bp.route('/<boat_id>/loads/<load_id>', methods=['PUT', 'DELETE'])
@require_jwt
def loads_on_boats(boat_id, load_id, payload):
    if payload is None:
        return '', 401

    load_key = client.key('Load', int(load_id))
    load = client.get(load_key)
    boat_key = client.key('Boat', int(boat_id))
    boat = client.get(boat_key)

    sub = payload['sub']
    if boat and not is_owner(boat, sub):
        return jsonify({"error": "The boat with this boat id is owned by another captain."}), 403

    if request.method == 'PUT':
        return assign_load_to_boat(boat, load)
    elif request.method == 'DELETE':
        return remove_load_from_boat(boat, load)


def is_owner(boat, sub):
    if boat['captain_id'] != sub:
        return False
    return True


def assign_load_to_boat(boat, load):
    if not boat or not load:
        return jsonify({"Error": "No load with this load_id exists or no boat with this "
                                 "boat_id exists."}), 404

    if load['carrier']:
        return jsonify({"Error": "The load is already loaded on another boat"}), 403
    boat['loads'].append({"id": load.id})
    load['carrier'] = {'id': boat.id}

    client.put(boat)
    client.put(load)

    return '', 204


def remove_load_from_boat(boat, load):
    if not load or not boat or not load['carrier']:
        return jsonify({"Error": "No boat with this boat_id is loaded with the load with "
                                 "this load_id."}), 404

    if load['carrier']['id'] != boat.id or \
            (len(boat['loads']) != 0 and load.id not in [k['id'] for k in list(boat['loads'])]):
        return jsonify({"Error": "No boat with this boat_id is loaded with the load with this load_id"}), 404

    load['carrier'] = None
    for l in boat['loads']:
        if l['id'] == load.id:
            boat['loads'].remove(l)

    client.put(boat)
    client.put(load)

    return '', 204
