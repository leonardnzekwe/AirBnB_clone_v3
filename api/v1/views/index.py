#!/usr/bin/python3
"""Index View"""
from api.v1.views import app_views
from flask import jsonify


# Create a route /status on the object app_views that returns a JSON response
@app_views.route('/status', methods=['GET'])
def get_status():
    """Get status Method"""
    return jsonify({"status": "OK"})
