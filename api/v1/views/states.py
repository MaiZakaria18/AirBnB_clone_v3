#!/usr/bin/python3
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def list_of_states():
    state_objects = storage.all(State).values()
    state_list = [state.to_dict() for state in state_objects]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def state(state_id):
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    return jsonify(state_object.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    storage.delete(state_object)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    if not request.is_json:
        abort(400, 'Request must be JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    new_state = State(**request.json)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.json
    for key, value in data.items():
        setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
