#!/usr/bin/python3
"""[methods for amenities routing]
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def RetrieveAllAmenities():
    """GET /amenities
    ---
    definitions:
      Amenities:
        type: object
    responses:
      200:
        description: A list of amenities
        schema:
          $ref: '#/definitions/Amenities'
    """
    objs = []
    amenity_values = storage.all("Amenity").values()
    for obj in amenity_values:
        objs.append(obj.to_dict())
    return jsonify(objs)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def RetrieveAmenityObject(amenity_id):
    """[RetrieveAmenityObject method]
    ---
    get:
        parameters:
          - name: amenity_id
            in: path
            type: string
            required: true
            default: all
    responses:
      200:
        description: get an amenity
    """
    amenity_values = storage.all("Amenity").values()
    if amenity_id is not None:
        for obj in amenity_values:
            if obj.id == amenity_id:
                return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def DeleteAmenity(amenity_id):
    """DELETE /amenities/:amenity_id
    ---
    delete:
        parameters:
          - name: amenity_id
            in: path
            type: string
            required: true
            default: all
    responses:
      200:
        description: Delete an amenity
    """
    deleted_amenity = storage.get("Amenity", amenity_id)
    if deleted_amenity:
        storage.delete(deleted_amenity)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def PostAmenity():
    """[post amenity method]
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
        description: post an amenity
    """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    elif "name" not in req.keys():
        abort(400, "Missing name")
    else:
        new_amenity = Amenity(**req)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def PutAmenity(amenity_id=None):
    """[PUT amenity method]
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
          - name: amenity_id
            in: path
            type: string
            required: true
            description: amenity id
        properties:
              key:
                type: string
                description: Unique identifier representing a key
              value:
                type: string
                description: Unique identifier representing a value
    responses:
      201:
        description: put an amenity
    """
    updated_amenity = storage.get("Amenity", amenity_id)
    if updated_amenity:
        req = request.get_json()
        if req is None:
            abort(400, "Not a JSON")
        for k, v in req.items():
            if k in ['id', 'created_at', 'updated_at']:
                pass
            setattr(updated_amenity, k, v)
        storage.save()
        return jsonify(updated_amenity.to_dict())
    abort(404)
