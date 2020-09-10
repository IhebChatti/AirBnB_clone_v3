#!/usr/bin/python3
"""[ view for the link between Place objects and
    Amenity objects that handles all default RestFul API actions]
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from os import getenv
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def GetAmenityOfPlace(place_id):
    """[GetAmenityOfPlace method]

    Args:
        place_id ([str]): [place id]

    Returns:
        [json/status]: [json and 200 on success, 404 on failure]
    """
    place = storage.get("Place", place_id)
    if place:
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def DeleteAmenityToPlace(place_id, amenity_id):
    """[DeleteAmenityToPlace]

    Args:
        place_id ([str]): [place id]
        amenity_id ([str]): [amenity id]

    Returns:
        [json/status]: [json and status of response]
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            storage.delete(amenity)
            storage.save()
            return jsonify({})
        abort(404)
    else:
        if amenity.id in place.amenity_ids:
            storage.delete(amenity)
            storage.save()
            return jsonify({})
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def AmenityToPlace(place_id, amenity_id):
    """[AmenityToPlace Method]

    Args:
        place_id ([str]): [place id]
        amenity_id ([str]): [amenity id]

    Returns:
        [json/status]: [json file nad status of response]
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            storage.save()
            return jsonify(amenity.to_dict())
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            storage.save()
            return jsonify(amenity.to_dict())
        else:
            place.amenity_ids.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
