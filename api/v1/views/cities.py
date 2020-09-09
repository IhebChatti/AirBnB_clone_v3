#!/usr/bin/python3
"""CityAPI"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['GET'])
def render_cities_by_state(state_id):
    """GET /states/:state_id/cities"""
    from models.state import State
    state = storage.get(State, state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])
    abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['GET'])
def render_city_by_id(city_id):
    """GET /cities/:city_id"""
    from models.city import City
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_city_by_id(city_id):
    """DELETE /cities/:city_id"""
    from models.city import City
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify(status=200)
    abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """POST /states/:state_id/cities"""
    from models.state import State
    state = storage.get(State, state_id)
    content = request.get_json()
    if not content:
        return jsonify({"error": "Not a JSON"}, status=400)
    if not 'name' in content:
        return jsonify({"error": "Missing name"}, status=400)
    city = BaseModel({
        'name': content['name']
    })
    city.save()
    return jsonify(city, status=200)
