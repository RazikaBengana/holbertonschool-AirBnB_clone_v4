#!/usr/bin/python3
"""Module that handles all operations related to places within the application context"""

from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route("/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def place_all(city_id=None):
    """Retrieve a list of all places in a specified city using the city's ID"""
    if city_id:
        city = storage.get(City, city_id)

        if city is not None:
            place_list = [place.to_dict() for place in city.places]
            return jsonify(place_list)
        return abort(404)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def place_by_id(place_id=None):
    """Retrieve a specific place by its ID"""
    if place_id:
        place = storage.get(Place, place_id)

        if place is not None:
            return jsonify(place.to_dict())
        return abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def place_delete(place_id):
    """Delete a specific place by its ID and return an empty JSON response on success"""
    place = storage.get(Place, place_id)

    if place is not None:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new place within a city specified by city_id, based on the provided JSON payload"""
    city = storage.get(City, city_id)

    if city is None:
        return abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    places = request.get_json()
    user = storage.get(User, places['user_id'])

    if user is None:
        abort(404)
    places['city_id'] = city_id
    place = Place(**places)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Update a place specified by place_id based on the provided JSON payload,
    excluding certain fields like id and timestamps
    """
    place = storage.get(Place, place_id)

    if place is None:
        return abort(404)
    request_dict = request.get_json()

    if request_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, val in request_dict.items():
        if key not in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
            setattr(place, key, val)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
