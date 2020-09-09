#!/usr/bin/python3
"""[methods for amenities routing]
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def RetrieveAllAmenities():
    """[RetrieveAllAmenities method]

    Returns:
        [json]: [list of all amenity objects]
    """
    amenities = storage.all("Amenity").values()
    if amenities:
        return jsonify([amenity.to_dict() for amenity in amenities])
    abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def RetrieveAmenityObject(amenity_id):
    """[RetrieveAmenityObject method]

    Args:
        amenity_id ([str]): [amenity id]

    Returns:
        [json]: [json rep of amenity on success, 404 on failure]
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def DeleteAmenity(amenity_id):
    """[delete request]

    Args:
        amenity_id ([str]): [amenity id]

    Returns:
        [json]: [200 on success or 404 status on failure]
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

    Returns:
        [status/json]: [json file and 200 status on success, 400 on failure]
    """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if "name" not in req:
        abort(400, "Missing name")
    new_amenity = Amenity(**req)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def PutAmenity(amenity_id=None):
    """[PUT amenity method]

    Args:
        amenity_id ([str], optional): [amenity id]. Defaults to None.

    Returns:
        [status/json]: [json file and 200 status on success, 400 on failure]
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
