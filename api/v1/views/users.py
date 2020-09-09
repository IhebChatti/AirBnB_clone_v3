#!/usr/bin/python3
"""[methods for users routing]
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.user import User


@app_views.route('/users', strict_slashes=False)
def RetrieveAllUsers():
    """[RetrieveAllUsers method]

    Returns:
        [json]: [list of all User objects]
    """
    objs = []
    users_values = storage.all("User").values()
    for obj in users_values:
        objs.append(obj.to_dict())
    return jsonify(objs)


@app_views.route('/users/<user_id>', strict_slashes=False)
def RetrieveUserObject(user_id):
    """[RetrieveUserObject method]

    Args:
        user_id ([str]): [user id]

    Returns:
        [json]: [json rep of user on success, 404 on failure]
    """
    users_values = storage.all("User").values()
    if user_id is not None:
        for obj in users_values:
            if obj.id == user_id:
                return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def DeleteUser(user_id):
    """[delete request]

    Args:
        user_id ([str]): [user id]

    Returns:
        [json]: [200 on success or 404 status on failure]
    """
    deleted_user = storage.get("User", user_id)
    if deleted_user:
        storage.delete(deleted_user)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def PostUser():
    """[post user method]

    Returns:
        [status/json]: [json file and 200 status on success, 400 on failure]
    """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    elif "email" not in req.keys():
        abort(400, "Missing email")
    elif "password" not in req.keys():
        abort(400, "Missing password")
    else:
        new_user = User(**req)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def PutUser(user_id=None):
    """[PUT user method]

    Args:
        user_id ([str], optional): [user id]. Defaults to None.

    Returns:
        [status/json]: [json file and 200 status on success, 400 on failure]
    """
    updated_user = storage.get("User", user_id)
    if updated_user is None:
        abort(400)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k in ['id', 'email', 'created_at', 'updated_at']:
            pass
        setattr(updated_user, k, v)
    storage.save()
    return jsonify(updated_user.to_dict())
