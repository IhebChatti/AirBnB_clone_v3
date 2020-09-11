#!/usr/bin/python3
"""[methods for places routing]
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def RetrieveAllPlaces(city_id=None):
    """GET /cities/:city_id/places
    ---
    parameters:
      - name: city_id
        in: path
        type: string
        required: true
        default: all
    definitions:
      Places:
        type: object
    responses:
      200:
        description: A list of places by city
        schema:
          $ref: '#/definitions/Places'
    """
    city = storage.get("City", city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def RetrievePlaceObject(place_id):
    """[RetrievePlaceObject method]
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
        default: ""
    definitions:
      Place:
        type: object
    responses:
      200:
        description: A place by ID
        schema:
          $ref: '#/definitions/Place'
    """
    places_values = storage.all("Place").values()
    if place_id is not None:
        for obj in places_values:
            if obj.id == place_id:
                return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def DeletePlace(place_id):
    """[delete request]
    ---
    delete:
        parameters:
          - name: place_id
            in: path
            type: string
            required: true
            default: all
    responses:
      200:
        description: Delete a place
    """
    deleted_place = storage.get("Place", place_id)
    if deleted_place:
        storage.delete(deleted_place)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def PostPlace(city_id):
    """[post place method]
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
          - name: city_id
            in: path
            required: true
            default: all
        properties:
              key:
                type: string
                description: Unique identifier representing a key
              value:
                type: string
                description: Unique identifier representing a value
    responses:
      201:
        description: post a place
    """
    from models.place import Place
    city = storage.get("City", city_id)
    if city:
        content = request.get_json()
        if not content:
            abort(400, "Not a JSON")
        if 'user_id' not in content:
            abort(400, "Missing user_id")
        user = storage.get("User", content['user_id'])
        if not user:
            abort(404)
        if 'name' not in content:
            abort(400, "Missing name")
        content['city_id'] = city.id
        place = Place(**content)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def PutPlace(place_id=None):
    """[PUT place method]
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
          - name: place_id
            in: path
            type: string
            required: true
            description: place id
        properties:
              key:
                type: string
                description: Unique identifier representing a key
              value:
                type: string
                description: Unique identifier representing a value
    responses:
      201:
        description: put a place
    """
    updated_place = storage.get("Place", place_id)
    if updated_place:
        req = request.get_json()
        if req is None:
            abort(400, "Not a JSON")
        for k, v in req.items():
            if k in ['id', 'user_id', 'city_id', 'created_at',
                     'updated_at']:
                pass
            setattr(updated_place, k, v)
        storage.save()
        return jsonify(updated_place.to_dict())
    abort(404)
