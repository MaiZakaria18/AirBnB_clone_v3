#!/usr/bin/python3
""" API """
from flask import jsonify
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
