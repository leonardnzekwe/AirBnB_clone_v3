#!/usr/bin/python3
"""Flask App Module"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


# Create a Flask instance
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)


# Create a handler for 404 errors that returns a JSON-formatted 404 response
@app.errorhandler(404)
def not_found(error):
    """Error handler message"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    # Get host and port from environment variables or use default values
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))

    # Run the Flask server with threaded=True
    app.run(host=host, port=port, threaded=True)
