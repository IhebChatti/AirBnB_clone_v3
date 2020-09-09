#!/usr/bin/python3
"""[methods for states routing]
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort


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

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def DeleteState(state_id):
    deleted_state = storage.get("State", state_id)
    if deleted_state:
        storage.delete(deleted_state)
        storage.save()
        return jsonify({})
    abort(404)
