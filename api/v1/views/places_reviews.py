#!/usr/bin/python3
"""ReviewAPI"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET'])
def render_reviews_by_place(place_id):
    """GET /places/:place_id/reviews
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
        default: all
    definitions:
      Reviews:
        type: object
    responses:
      200:
        description: A list of reviews by places
        schema:
          $ref: '#/definitions/Reviews'
    """
    place = storage.get("Place", place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['GET'])
def render_review_by_id(review_id):
    """GET /reviews/:review_id"""
    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_review_by_id(review_id):
    """DELETE /reviews/:review_id"""
    review = storage.get("Review", review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """POST /places/:place_id/reviews"""
    from models.review import Review
    place = storage.get("Place", place_id)
    if place:
        content = request.get_json()
        if not content:
            abort(400, "Not a JSON")
        if 'user_id' not in content:
            abort(400, "Missing user_id")
        user = storage.get("User", content['user_id'])
        if not user:
            abort(404)
        if 'text' not in content:
            abort(400, "Missing text")
        content['place_id'] = place.id
        review = Review(**content)
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """PUT /reviews/:review_id"""
    review = storage.get("Review", review_id)
    if review:
        content = request.get_json()
        if content is None:
            abort(400, "Not a JSON")
        for key, value in content.items():
            if key in ['id', 'place_id', 'user_id', 'created_at',
                       'updated_at']:
                pass
            setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict())
    abort(404)
