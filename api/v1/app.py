#!/usr/bin/python3
""" API """

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
    return storage.close()


if __name__ == "__main__":
    if getenv("HBNB_API_HOST"):
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    else:
        HBNB_API_HOST = '0.0.0.0'
    if getenv("HBNB_API_PORT"):
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    else:
        HBNB_API_PORT = 5000
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
