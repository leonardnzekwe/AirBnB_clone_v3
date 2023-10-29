#!/usr/bin/python3
"""Index View For Flask"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


# Create a route /status on the object app_views that returns a JSON response
@app_views.route('/status', methods=['GET'])
def get_status():
    """Get status Method"""
    return jsonify({"status": "OK"})


# Create a route /stats that retrieves the count of each object type
@app_views.route('/stats', methods=['GET'])
def get_stats():
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
