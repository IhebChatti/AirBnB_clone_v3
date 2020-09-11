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
    """GET /places/:place_id/amenities
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
        default: all
    definitions:
      Amenities:
        type: object
    responses:
      200:
        description: A list of amenities by places
        schema:
          $ref: '#/definitions/Amenities'
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
    ---
    delete:
        parameters:
          - name: place_id
            in: path
            type: string
            required: true
            default: all
          - name: amenity_id
            in: path
            type: string
            required: true
            default: all
    responses:
      200:
        description: Delete a place_amenity
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
          - name: place_id
            in: path
            required: true
            default: ""
          - name: amenity_id
            in: path
            required: true
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
        description: post a place_amenity
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
