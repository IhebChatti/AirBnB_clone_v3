#!/usr/bin/python3
"""[methods for states routing]
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.state import State


@app_views.route('/states', strict_slashes=False)
def RetrieveAllStates():
    """[RetrieveAllStates method]

    Returns:
        [json]: [list of all State objects]
    """
    objs = []
    states_values = storage.all("State").values()
    for obj in states_values:
        objs.append(obj.to_dict())
    return jsonify(objs)


@app_views.route('/states/<state_id>', strict_slashes=False)
def RetrieveStateObject(state_id):
    """[RetrieveState method]

    Args:
        state_id ([str]): [state id]

    Returns:
        [json]: [json rep of state on success, 404 on failure]
    """
    states_values = storage.all("State").values()
    if state_id is not None:
        for obj in states_values:
            if obj.id == state_id:
                return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def DeleteState(state_id):
    """[delete request]

    Args:
        state_id ([str]): [state id]

    Returns:
        [json]: [200 on success or 404 status on failure]
    """
    deleted_state = storage.get("State", state_id)
    if deleted_state:
        storage.delete(deleted_state)
        try:
            storage.save()
        except:
            storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def PostState():
    """[post state method]

    Returns:
        [status/json]: [json file and 200 status on success, 400 on failure]
    """
    req = request.get_json(silent=True)
    if req is None:
        abort(400, "Not a JSON")
    elif "name" not in req.keys():
        abort(400, "missing name")
    else:
        new_state = State(**req)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict())


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def PutState(state_id=None):
    """[PUT state method]

    Args:
        state_id ([str], optional): [state id]. Defaults to None.

    Returns:
        [status/json]: [json file and 200 status on success, 400 on failure]
    """
    updated_state = storage.get("State", state_id)
    if updated_state is None:
        abort(400)
    req = request.get_json(silent=True)
    if req is None:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k in ['id', 'created_at', 'updated_at']:
            pass
        setattr(updated_state, k, v)
    storage.save()
    return jsonify(updated_state.to_dict())
