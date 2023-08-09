#!/usr/bin/python3
""" objects that handles all default RestFul API actions for streets """
from models.street import Street
from models.location import Location
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/locations/<location_id>/streets', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/street/streets_by_location.yml', methods=['GET'])
def get_streets(location_id):
    """
    Retrieves the list of all streets objects
    of a specific Location, or a specific street
    """
    list_streets = []
    location = storage.get(Location, location_id)
    if not location:
        abort(404)
    for street in location.streets:
        list_streets.append(street.to_dict())

    return jsonify(list_streets)


@app_views.route('/streets/<street_id>/', methods=['GET'], strict_slashes=False)
@swag_from('documentation/street/get_street.yml', methods=['GET'])
def get_street(street_id):
    """
    Retrieves a specific street based on id
    """
    street = storage.get(Street, street_id)
    if not street:
        abort(404)
    return jsonify(street.to_dict())


@app_views.route('/streets/<street_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/street/delete_street.yml', methods=['DELETE'])
def delete_street(street_id):
    """
    Deletes a street based on id provided
    """
    street = storage.get(Street, street_id)

    if not street:
        abort(404)
    storage.delete(street)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/locations/<location_id>/streets', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/street/post_street.yml', methods=['POST'])
def post_street(location_id):
    """
    Creates a Street
    """
    location = storage.get(Location, location_id)
    if not location:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Street(**data)
    instance.location_id = location.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/streets/<street_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/street/put_street.yml', methods=['PUT'])
def put_street(street_id):
    """
    Updates a Street
    """
    street = storage.get(Street, street_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'location_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(street, key, value)
    storage.save()
    return make_response(jsonify(street.to_dict()), 200)
