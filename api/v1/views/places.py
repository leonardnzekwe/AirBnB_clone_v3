#!/usr/bin/python3
""" Place view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False
    )
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False
    )
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False
    )
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if data is None:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    if "name" not in data:
        abort(400, description="Missing name")

    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if data is None:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route(
        '/places_search', methods=['POST'], strict_slashes=False
    )
def places_search():
    """Search for places based on JSON criteria in the request body."""
    try:
        search_params = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    if not search_params or all(len(v) == 0 for v in search_params.values()):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    places = set()

    # Search by states
    if 'states' in search_params:
        states = storage.get(State, search_params['states'])
        for state in states:
            places.update(state.places)

    # Search by cities
    if 'cities' in search_params:
        cities = storage.get(City, search_params['cities'])
        places.update(cities.places)

    # Search by amenities
    if 'amenities' in search_params:
        amenities = storage.get(Amenity, search_params['amenities'])
        for amenity in amenities:
            places.intersection_update(amenity.places)

    return jsonify([place.to_dict() for place in places])
