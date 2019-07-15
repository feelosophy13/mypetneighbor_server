from flask import Blueprint
from flask import request, jsonify
from pprint import pprint
from bson.objectid import ObjectId
from bson.json_util import dumps
import json

from mpn import app
from mpn.models import User, Pet, Dog
from mpn.helper_funcs.helper import token_required, admin_only

pet_blueprint = Blueprint("pet_blueprint", __name__)


@pet_blueprint.route("/user/<user_id>/pets/", methods=["GET"])
def get_user_pets(user_id):

    # get user
    try:
        user = User.objects.get(id=user_id)
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })

    # get pets
    pets_list = []
    for pet in Pet.objects(owner=user):
        pets_list.append(json.loads(pet.to_json()))

    # return json 
    return jsonify({
        "status": "success",
        "pets": pets_list
    })
    

@pet_blueprint.route("/pet/add/", methods=["POST"])
@token_required
def add_pet(current_user):

    # get provided data
    data = request.get_json()

    # create and add pet 
    dog = Dog(
        name = data.get("name"),
        owner = current_user,
        birth_year = data.get("birth_year"),
        gender = data.get("gender"),
        potty_trained = data.get("potty_trained"),
        neutered = data.get("neutered"),
        aggression_level = data.get("aggression_level"),
        breed = data.get("breed"),
        weight_lb = data.get("weight_lb")
    )
    dog.save()

    # return data
    return jsonify({
        "status": "success",
        "message": "record added",
        "pet": json.loads(dog.to_json())
    })


@pet_blueprint.route("/pet/<pet_id>/", methods=["GET"])
def get_pet(pet_id):

    # get pet
    try:
        pet = Pet.objects.get(id=pet_id)
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })

    # return data
    return jsonify({
        "status": "success",
        "pet": json.loads(pet.to_json())
    })


@pet_blueprint.route("/pet/<pet_id>/update/", methods=["PUT"])
@token_required
def update_pet(current_user, pet_id):

    # get pet
    try:
        pet = Pet.objects.get(id=pet_id, owner__id=current_user.id)
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })

    # get provided data
    data = request.get_json()

    # update and save
    pet.name = data.get("name")
    pet.birth_year = data.get("birth_year")
    pet.gender = data.get("gender")
    pet.potty_trained = data.get("potty_trained")
    pet.neutered = data.get("neutered")
    pet.aggression_level = data.get("aggression_level")
    pet.breed = data.get("breed")
    pet.weight_lb = data.get("weight_lb")
    pet.save()

    # upon successful update
    return jsonify({
        "status": "success",
        "message": "record updated",
        "pet_id": pet_id
    })


@pet_blueprint.route("/pet/<pet_id>/delete/", methods=["DELETE"])
@token_required
def delete_pet(current_user, pet_id):

    # get pet
    try:
        pet = Pet.objects.get(id=pet_id, owner__id=current_user.id)
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })

    # delete in db
    pet.delete()

    # upon successful delete
    return jsonify({
        "status": "success",
        "message": "record deleted",
        "pet_id": pet_id
    })
