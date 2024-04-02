#!/usr/bin/python3
"""
Handles all RESTful API actions for `User` objects
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_of_user():
    """Retrieve the list of all `user` objects"""
    user_objects = storage.all(User).values()
    user_objects = [user.to_dict() for user in user_objects]
    return jsonify(user_objects)


@app_views.route('/users/<users_id>', methods=['GET'])
def users(users_id):
    """Retrieve the `users` objects"""
    users_object = storage.get(User, users_id)
    if users_object is None:
        abort(404)
    return jsonify(users_object.to_dict())


@app_views.route('/users/<users_id>', methods=['DELETE'])
def users_delete(users_id):
    """Delete a users object"""
    users_object = storage.get(User, users_id)
    if users_object is None:
        abort(404)
    storage.delete(users_object)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_users():
    """Create a `users` object"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    new_users = User(**request.json)
    storage.new(new_users)
    storage.save()
    return jsonify(new_users.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_users(user_id):
    """Update `users` object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.json
    for key, value in data.items():
        setattr(users, key, value)
    storage.save()
    return jsonify(users.to_dict()), 200
