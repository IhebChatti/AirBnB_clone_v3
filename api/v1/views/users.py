#!/usr/bin/python3
"""[methods for users routing]
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.user import User


@app_views.route('/users', strict_slashes=False)
def RetrieveAllUsers():
    """GET /users
    ---
    definitions:
      Users:
        type: object
    responses:
      200:
        description: A list of users
        schema:
          $ref: '#/definitions/Users'
    """
    objs = []
    users_values = storage.all("User").values()
    for obj in users_values:
        objs.append(obj.to_dict())
    return jsonify(objs)


@app_views.route('/users/<user_id>', strict_slashes=False)
def RetrieveUserObject(user_id):
    """[RetrieveUserObject method]
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        default: all
    definitions:
      User:
        type: object
    responses:
      200:
        description: A user by ID
        schema:
          $ref: '#/definitions/User'
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
    ---
    delete:
        parameters:
          - name: user_id
            in: path
            type: string
            required: true
            default: all
    responses:
      200:
        description: Delete a user
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
    ---
    post:
        consumes:
            - application/json
        parameters:
          - name: body
            in: body
            required:
              - key
              - value
            default: ""
        properties:
              key:
                type: string
                description: Unique identifier representing a key
              value:
                type: string
                description: Unique identifier representing a value
    responses:
      201:
        description: post a user
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
    ---
    put:
        consumes:
            - application/json
        parameters:
          - name: body
            in: body
            required:
              - key
              - value
            default: ""
          - name: user_id
            in: path
            type: string
            required: true
            description: user id
        properties:
              key:
                type: string
                description: Unique identifier representing a key
              value:
                type: string
                description: Unique identifier representing a value
    responses:
      201:
        description: put a user
    """
    updated_user = storage.get("User", user_id)
    if updated_user:
        req = request.get_json()
        if req is None:
            abort(400, "Not a JSON")
        for k, v in req.items():
            if k in ['id', 'email', 'created_at', 'updated_at']:
                pass
            setattr(updated_user, k, v)
        storage.save()
        return jsonify(updated_user.to_dict())
    abort(404)
