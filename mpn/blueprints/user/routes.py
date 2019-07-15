from flask import Blueprint
from flask import request, jsonify
import json, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from geopy.geocoders import Nominatim

from mpn import app#, mongo
from mpn.helper_funcs.helper import token_required, admin_only
from mpn.models import User, PetSitAvailability
#from mpn.blueprints.user.helper import get_geo_coordinates
#from mpn.config import GOOGLE_GEOCODING_API_KEY


user_blueprint = Blueprint("user_blueprint", __name__)


# https://stackoverflow.com/a/46753715
# http://docs.mongoengine.org/guide/querying.html?highlight=near
@user_blueprint.route("/users/nearby/<float(signed=True):longitude>/<float(signed=True):latitude>/<max_distance>/", methods=["GET"])
def get_nearby_users(longitude, latitude, max_distance):
    users_data = []    
    for user in User.objects(coordinates__near=[longitude, latitude], coordinates__max_distance=int(max_distance)):
        users_data.append(json.loads(user.to_json()))
    return jsonify({
        "status": "success",
        "users": users_data
    })

@user_blueprint.route("/users/", methods=["GET"])
def get_users():
    users_data = []
    for user in User.objects:
        users_data.append(json.loads(user.to_json()))
    return jsonify({
        "status": "success",
        "users": users_data
    })


@user_blueprint.route("/user/add/", methods=["POST"])
def add_user():

    # get provided data
    data = request.get_json()

    # hash password
    hashed_password = generate_password_hash(data["password"], method="sha256")

    # get geographic coordinates 
    #coordinates = get_geo_coordinates(address=address, api_key=GOOGLE_GEOCODING_API_KEY)
    geolocator = Nominatim()    
    location = geolocator.geocode(f'{data["address"]}, {data["city"]}, {data["state"]} {data["postal_code"]}')

    # create and add user
    user = User(
        name = data["name"],
        email_address = data["email_address"],
        password_hashed = hashed_password,
        address = data["address"],
        city = data["city"],
        state = data["state"],
        postal_code = data["postal_code"],
        coordinates = [location.longitude, location.latitude]
    )
    user.save()

    # create and add pet-sit availability
    petsit_availability = PetSitAvailability(user = user)
    petsit_availability.save()

    return jsonify({
        "status": "success",
        "message": "record created",
        "user_id": str(user.id)
    })


@user_blueprint.route("/user/update-availability/", methods=["PUT"])
@token_required
def update_user_availability(current_user):

    # get provided data
    data = request.get_json()

    # update data
    petsit_availability = PetSitAvailability(user = user)
    petsit_availability.monday = data.get("monday")
    petsit_availability.tuesday = data.get("tuesday")
    petsit_availability.wednesday = data.get("wednesday")
    petsit_availability.thursday = data.get("thursday")
    petsit_availability.friday = data.get("friday")
    petsit_availability.saturday = data.get("saturday")
    petsit_availability.sunday = data.get("sunday")
    petsit_availability.at_night = data.get("at_night")
    petsit_availability.save()

    # return json result
    return jsonify({
        "status": "success",
        "message": "record updated",
        "petsit_availability": json.loads(petsit_availability.to_json())
    })


@user_blueprint.route("/user/update/", methods=["PUT"])
@token_required
def update_user(current_user):

    # get provided data
    data = request.get_json()

    # update
    current_user.name = data.get("name")
    current_user.email_address = data.get("email_address")
    current_user.password_hashed = generate_password_hash(data.get("password"), method="sha256")
    current_user.address = data.get("address")
    current_user.city = data.get("city")
    current_user.state = data.get("state")
    current_user.postal_code = data.get("postal_code")
    current_user.save()

    # return json result
    return jsonify({
        "status": "success",
        "message": "record updated",
        "user_id": str(current_user.id)
    })


@user_blueprint.route("/user/<user_id>/", methods=["GET"])
def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })
    return jsonify({
        "status": "success",
        "user": json.loads(user.to_json())
    })



@user_blueprint.route("/user/delete/", methods=["DELETE"])
@token_required
def delete_user(current_user):
    current_user.delete()
    return jsonify({
        "status": "success",
        "message": "record deleted"
    })

