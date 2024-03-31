#!/usr/bin/python3
""" API """

from flask import jsonify
from models import storage

from . import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """ returns status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def count_class():
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    obj_dic = {}
    for key in classes:
        obj_dic[classes[key]] = storage.count(key)
        return jsonify(obj_dic)
