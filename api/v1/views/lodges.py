#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Places """
from models.location import Location
from models.street import Street
from models.lodge import Lodge
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/streets/<street_id>/lodges', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/lodge/get_lodges.yml', methods=['GET'])
def get_lodges(street_id):
    """
    Retrieves the list of all Lodge objects of a Street
    """
    street = storage.get(Street, street_id)

    if not street:
        abort(404)

    lodges = [lodge.to_dict() for lodge in street.lodges]

    return jsonify(lodges)


@app_views.route('/lodges/<lodge_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/lodge/get_lodge.yml', methods=['GET'])
def get_lodge(lodge_id):
    """
    Retrieves a Lodge object
    """
    lodge = storage.get(Lodge, lodge_id)
    if not lodge:
        abort(404)

    return jsonify(lodge.to_dict())


@app_views.route('/lodges/<lodge_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/lodge/delete_lodge.yml', methods=['DELETE'])
def delete_lodge(lodge_id):
    """
    Deletes a Lodge Object
    """

    lodge = storage.get(Lodge, lodge_id)

    if not lodge:
        abort(404)

    storage.delete(lodge)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/streets/<street_id>/lodges', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/lodge/post_lodge.yml', methods=['POST'])
def post_lodge(street_id):
    """
    Creates a Lodge
    """
    street = storage.get(Street, street_id)

    if not street:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data["street_id"] = street_id
    instance = Lodge(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/lodges/<lodge_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/lodge/put_lodge.yml', methods=['PUT'])
def put_lodge(lodge_id):
    """
    Updates a Lodge
    """
    lodge = storage.get(Lodge, lodge_id)

    if not lodge:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(lodge, key, value)
    storage.save()
    return make_response(jsonify(lodge.to_dict()), 200)


@app_views.route('/lodges_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/lodge/post_search.yml', methods=['POST'])
def lodges_search():
    """
    Retrieves all Lodge objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        locations = data.get('locations', None)
        streets = data.get('streets', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not locations and
            not streets and
            not amenities):
        lodges = storage.all(Lodge).values()
        list_lodges = []
        for lodge in lodges:
            list_lodges.append(lodge.to_dict())
        return jsonify(list_lodges)

    list_lodges = []
    if locations:
        locations_obj = [storage.get(Location, l_id) for l_id in locations]
        for location in locations_obj:
            if location:
                for street in location.streets:
                    if street:
                        for lodge in street.lodges:
                            list_lodges.append(lodge)

    if streets:
        street_obj = [storage.get(Street, s_id) for s_id in streets]
        for street in street_obj:
            if street:
                for lodgee in street.lodges:
                    if lodge not in list_lodges:
                        list_lodges.append(lodge)

    if amenities:
        if not list_lodges:
            list_lodges = storage.all(Lodge).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_lodges = [lodge for lodge in list_lodges
                       if all([am in lodge.amenities
                               for am in amenities_obj])]

    lodges = []
    for l in list_lodges:
        d = l.to_dict()
        d.pop('amenities', None)
        lodges.append(d)

    return jsonify(lodges)
