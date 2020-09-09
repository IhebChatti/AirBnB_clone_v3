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
    """[RetrieveAllPlaces method]

    Returns:
        [json]: [list of all Place objects]
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

    Args:
        place_id ([str]): [place id]

    Returns:
        [json]: [json rep of place on success, 404 on failure]
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

    Args:
        place_id ([str]): [place id]

    Returns:
        [json]: [200 on success or 404 status on failure]
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

    Returns:
        [status/json]: [json file and 200 status on success, 400 on failure]
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

    Args:
        place_id ([str], optional): [place id]. Defaults to None.

    Returns:
        [status/json]: [json file and 200 status on success, 400 on failure]
    """
    updated_place = storage.get("Place", place_id)
    if updated_place is None:
        abort(400)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            pass
        setattr(updated_place, k, v)
    storage.save()
    return jsonify(updated_place.to_dict())
