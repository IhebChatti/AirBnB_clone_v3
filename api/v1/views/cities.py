#!/usr/bin/python3
"""CityAPI"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['GET'])
def render_cities_by_state(state_id):
    """GET /states/:state_id/cities
    ---
    parameters:
      - name: state_id
        in: path
        type: string
        required: true
        default: all
    definitions:
      Cities:
        type: object
    responses:
      200:
        description: A list of cities
        schema:
          $ref: '#/definitions/Cities'
    """
    state = storage.get("State", state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])
    abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['GET'])
def render_city_by_id(city_id):
    """GET /cities/:city_id"""
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_city_by_id(city_id):
    """DELETE /cities/:city_id"""
    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """POST /states/:state_id/cities"""
    from models.city import City
    state = storage.get("State", state_id)
    if state:
        content = request.get_json()
        if not content:
            abort(400, "Not a JSON")
        if 'name' not in content:
            abort(400, "Missing name")
        content['state_id'] = state.id
        city = City(**content)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """PUT /cities/:city_id"""
    city = storage.get("City", city_id)
    if city:
        content = request.get_json()
        if content is None:
            abort(400, "Not a JSON")
        for key, value in content.items():
            if key in ['id', 'state_id', 'created_at',
                       'updated_at']:
                pass
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict())
    abort(404)
