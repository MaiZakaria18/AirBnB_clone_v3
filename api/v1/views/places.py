#!/usr/bin/python3
"""
Handles all RESTful API actions for `places` objects
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.places import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_of_places(city_id):
    """Retrieve the list of all `places` objects"""
    list_places = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for place in city.places:
        list_places.append(place.to_dict())

    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieving a specific place based on id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id):
    """Delete a place_object"""
    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404)
    storage.delete(place_object)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    data = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if not storage.get(User, data["user_id"]):
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")

    place = Place(city_id=city_id, **data)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update `place` object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.json
    for key, value in data.items():
        setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
