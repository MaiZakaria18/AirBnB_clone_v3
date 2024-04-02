#!/usr/bin/python3
"""
Handles all RESTful API actions for `Amenity` objects
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_of_amenity():
    """Retrieve the list of all `Amenity` objects"""
    amenities_objects = storage.all(Amenity).values()
    amenities_list = [amenities.to_dict() for amenities in amenities_objects]
    return jsonify(amenities_list)


@app_views.route('amenities/<amenity_id>', methods=['GET'])
def amenity(amenity_id):
    """Retrieve the `amenity` objects"""
    amenity_object = storage.get(Amenity, amenity_id)
    if amenity_object is None:
        abort(404)
    return jsonify(amenity_object.to_dict())


@app_views.route('amenities/<amenity_id>', methods=['DELETE'])
def amenity_delete(amenity_id):
    """Delete a amenity_object"""
    amenity_object = storage.get(Amenity, amenity_id)
    if amenity_object is None:
        abort(404)
    storage.delete(amenity_object)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenities():
    """Create a `amenities` object"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    new_amenities = Amenity(**request.json)
    storage.new(new_amenities)
    storage.save()
    return jsonify(new_amenities.to_dict()), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update `amenity` object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.json
    for key, value in data.items():
        setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
