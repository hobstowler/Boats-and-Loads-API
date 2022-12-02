import flask
from flask import Blueprint, request, jsonify
from google.cloud import datastore

from verification import require_jwt

client = datastore.Client()

bp = Blueprint('loads', __name__, url_prefix='/loads')


@bp.route('/', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def loads():
    if not request.accept_mimetypes.accept_json:
        return '', 406

    if request.method == 'GET':
        return get_loads(request)
    elif request.method == 'POST':
        if not request.is_json:
            return '', 415
        return create_load(request)
    else:
        return '', 405


def get_loads(request: flask.Request):
    query = client.query(kind="Load")
    #query.add_filter('carrier', '=', None)
    total = len(list(query.fetch()))
    limit = int(request.args.get('limit', '5'))
    offset = int(request.args.get('offset', '0'))
    l_iterator = query.fetch(limit=limit, offset=offset)
    pages = l_iterator.pages
    loads = list(next(pages))
    if l_iterator.next_page_token:
        new_offset = offset + limit
        next_url = f'{request.base_url}?limit={limit}&offset={new_offset}'
    else:
        next_url = None

    results = []
    for load in loads:
        res = dict(load)
        if load['carrier']:
            load['carrier']['self'] = f'{request.host_url}boats/{load["carrier"]["id"]}'
        res['id'] = load.id
        res['self'] = f'{request.host_url}loads/{load.id}'
        results.append(res)
    output = {
        "next": next_url,
        "total": total,
        "loads": results
    }
    return jsonify(output)


def create_load(request: flask.Request):
    json = request.get_json()
    try:
        volume = json['volume']
        try:
            volume = int(volume)
        except ValueError:
            return jsonify({'error': 'Volume must be an integer.'}), 400
        item = json['item']
        creation_date = json['creation_date']
    except KeyError as e:
        return jsonify({'Error': "The request object is missing at least one of the required attributes"}), 400
    else:
        load = datastore.Entity(client.key("Load"))
        load.update({
            'volume': volume,
            'item': item,
            'creation_date': creation_date,
            'carrier': None
        })
        client.put(load)
        res = dict(load)
        res['id'] = load.id
        res['self'] = f'{request.base_url}{load.id}'
        return jsonify(res), 201


@bp.route('/<load_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def load(load_id: str):
    key = client.key('Load', int(load_id))
    load = client.get(key)

    # if load does not exist, then 404
    if not load:
        return jsonify({'Error': "No load with this load_id exists"}), 404

    if request.method == 'GET':
        if not request.accept_mimetypes.accept_json:
            return '', 406
        return get_load(load)
    elif request.method in ['PUT', 'PATCH']:
        if not request.accept_mimetypes.accept_json:
            return '', 406
        if not request.is_json:
            return '', 415
        if request.method == 'PUT':
            return put_load(load)
        elif request.method == 'PATCH':
            return patch_load(load)
    elif request.method == 'DELETE':
        return delete_load(key, load)


def get_load(load):
    res = dict(load)
    res['id'] = load.id
    res['self'] = f'{request.host_url}loads/{load.id}'

    if load['carrier']:
        key = client.key('Boat', int(load['carrier']['id']))
        boat = client.get(key)
        res['carrier'] = {
            'id': boat.id,
            'name': boat['name'],
            'self': f'{request.host_url}boats/{boat.id}'
        }

    return jsonify(res), 200


def put_load(load):
    json = request.get_json()
    try:
        volume = json['volume']
        try:
            volume = int(volume)
        except ValueError:
            return jsonify({'error': 'Volume must be an integer.'}), 400
        item = json['item']
        creation_date = json['creation_date']
    except KeyError as e:
        return jsonify({'Error': "The request object is missing at least one of the required attributes"}), 400
    else:
        load['volume'] = volume
        load['item'] = item
        load['creation_date'] = creation_date
        client.put(load)

        res = dict(load)
        res['id'] = load.id
        res['self'] = f'{request.host_url}loads/{load.id}'

        return jsonify(res), 200


def patch_load(load):
    json = request.json
    creation_date = json['creation_date'] if 'creation_date' in json else None
    item = json['item'] if 'item' in json else None
    if 'volume' in json:
        try:
            volume = int(json['volume'])
        except ValueError:
            return jsonify({'error': 'Volume must be an integer.'}), 400
    else:
        volume = None

    load['creation_date'] = creation_date if creation_date else load['creation_date']
    load['item'] = item if item else load['item']
    load['volume'] = volume if volume else load['volume']
    client.put(load)

    res = dict(load)
    res['id'] = load.id
    res['self'] = f'{request.host_url}loads/{load.id}'

    return jsonify(res), 200


def delete_load(key, load):
    if load['carrier']:
        boat_id = load['carrier']['id']
        boat_key = client.key('Boat', int(boat_id))
        boat = client.get(boat_key)
        for l in boat['loads']:
            if l['id'] == load.id:
                boat['loads'].remove(l)
            client.put(boat)

    client.delete(key)
    return jsonify({}), 204
