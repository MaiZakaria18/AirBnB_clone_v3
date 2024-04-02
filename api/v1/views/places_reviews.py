#!/usr/bin/python3
"""
Handles all RESTful API actions for `Review` objects
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def list_of_reviews(place_id):
    """Retrieve the list of all `Review` objects"""
    list_reviews = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for reviews in place.reviews:
        list_reviews.append(reviews.to_dict())

    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_reviews(review_id):
    """
    Retrieving a specific place based on id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def review_delete(review_id):
    """Delete a place_object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    data = request.get_json()
    if not place:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if not storage.get(User, data["user_id"]):
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")

    review = Review(place_id=place_id, **data)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_reviews(review_id):
    """Update `place` object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.json
    for key, value in data.items():
        setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
