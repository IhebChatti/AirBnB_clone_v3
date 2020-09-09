#!/usr/bin/python3
"""[python script to set flask app]
"""
from flask import Flask, Blueprint, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(error):
    """teardown method"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Error handling with 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(getenv('HBNB_API_HOST'), getenv('HBNB_API_PORT'), threaded=True)
