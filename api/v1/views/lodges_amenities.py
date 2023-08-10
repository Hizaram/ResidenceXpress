#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Lodge - Amenity """
from models.lodge import Lodge
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('lodges/<lodge_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/lodge_amenity/get_lodge_amenities.yml',
           methods=['GET'])
def get_lodge_amenities(lodge_id):
    """
    Retrieves the list of all Amenity objects of a Lodge
    """
    lodge = storage.get(Lodge, lodge_id)

    if not lodge:
        abort(404)

    if environ.get('TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in lodge.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in lodge.amenity_ids]

    return jsonify(amenities)


@app_views.route('/lodges/<lodge_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/lodge_amenity/delete_lodge_amenities.yml',
           methods=['DELETE'])
def delete_lodge_amenity(lodge_id, amenity_id):
    """
    Deletes a Amenity object of a Lodge
    """
    lodge = storage.get(Lodge, lodge_id)

    if not lodge:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if environ.get('TYPE_STORAGE') == "db":
        if amenity not in lodge.amenities:
            abort(404)
        lodge.amenities.remove(amenity)
    else:
        if amenity_id not in lodge.amenity_ids:
            abort(404)
        lodge.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/lodges/<lodge_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/lodge_amenity/post_lodge_amenities.yml',
           methods=['POST'])
def post_lodge_amenity(lodge_id, amenity_id):
    """
    Link a Amenity object to a Lodge
    """
    lodge = storage.get(Lodge, lodge_id)

    if not lodge:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if environ.get('TYPE_STORAGE') == "db":
        if amenity in lodge.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            lodge.amenities.append(amenity)
    else:
        if amenity_id in lodge.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            lodge.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
