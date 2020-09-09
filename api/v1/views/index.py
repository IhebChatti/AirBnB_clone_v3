#!/usr/bin/python3
"""[a script to route /status on the object app_views]
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """[status route]

    Returns:
        [json]: [json status]
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def render_stats():
    """Returns stats about classes"""
    stats = {
      "amenities": storage.count('Amenity'),
      "cities": storage.count('City'),
      "places": storage.count('Place'),
      "reviews": storage.count('Review'),
      "states": storage.count('State'),
      "users": storage.count('User')
    }
    return jsonify(stats)
