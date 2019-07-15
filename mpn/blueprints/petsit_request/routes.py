from flask import Blueprint
from flask import request, jsonify
import json, datetime

from mpn import app#, mongo
from mpn.helper_funcs.helper import token_required, admin_only
from mpn.models import User, PetSitAvailability, PetSitRequestSlot, PetSitRequest


petsit_request_blueprint = Blueprint("petsit_request_blueprint", __name__)


@petsit_request_blueprint.route("/petsit-requests/sent/", methods=["GET"])
@token_required
def list_petsit_requests_sent(current_user):
    petsit_requests_data = []
    for petsit_request in PetSitRequest.objects(requester = current_user):
        petsit_requests_data.append(json.loads(petsit_request.to_json()))
    return jsonify({
        "status": "success",
        "petsit_requests": petsit_requests_data
    })


@petsit_request_blueprint.route("/petsit-requests/received/", methods=["GET"])
@token_required
def list_petsit_requests_received(current_user):
    petsit_requests_data = []
    for petsit_request in PetSitRequest.objects(recipient = current_user):
        petsit_requests_data.append(json.loads(petsit_request.to_json()))
    return jsonify({
        "status": "success",
        "petsit_requests": petsit_requests_data
    })


@petsit_request_blueprint.route("/petsit-request/add/", methods=["POST"])
@token_required
def send_petsit_request(current_user):

    # get provided data
    data = request.get_json()

    # get user
    try:
        recipient = User.objects.get(id=data.get("recipient_id"))
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })

    # create a list of petsit request slots
    petsit_request_slots_list = []
    for slot in data.get("request_slots"):
        petsit_request_slot = PetSitRequestSlot(
            start_datetime = datetime.datetime.strptime(slot["start_datetime"], '%Y-%m-%d %H:%M:%S'),
            end_datetime = datetime.datetime.strptime(slot["end_datetime"], '%Y-%m-%d %H:%M:%S')
        )
        petsit_request_slots_list.append(petsit_request_slot)

    # create and save
    petsit_request = PetSitRequest(
        requester = current_user,
        recipient = recipient,
        points_offered = data.get("points_offered"),
        request_message = data.get("request_message"),
        request_slots = petsit_request_slots_list
    )
    petsit_request.save()

    # return json result
    return jsonify({
        "status": "success",
        "message": "record added",
        "petsit_request_id": str(petsit_request.id)
    })


@petsit_request_blueprint.route("/petsit-request/<petsit_request_id>/update/", methods=["POST"])
@token_required
def respond_petsit_request(current_user, petsit_request_id):

    # get provided data
    data = request.get_json()

    # get petsit request 
    try:
        petsit_request = PetSitRequest.object.get(id=petsit_request_id)
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })

    # if user made the pet request
    if petsit_request.requester == current_user:
        petsit_request.points_offered = data.get("points_offered")
        petsit_request.request_message = data.get("request_message")
        petsit_request.request_slots = data.get("request_slots")

    # if user received the pet request
    elif petsit_request.recipient == current_user:
        petsit_request.response = data.get("response")
        petsit_request.response_reason = data.get("response_reason")
        petsit_request.response_message = data.get("response_message")
        #petsit_request.fulfillment_status = data.get("fulfillment_status")

    else:
        return jsonify({
            "status": "error",
            "message": "You don't have access"
        })
    petsit_request.save()

    return jsonify({
        "status": "success",
        "message": "record updated"
    })




@petsit_request_blueprint.route("/user/petsit_request/<petsit_request_id>/delete/", methods=["DELETE"])
@token_required
def delete_petsit_request(current_user, petsit_request_id):

    try:
        petsit_request = PetSitRequest.object.get(id=petsit_request_id, requester__id=current_user.id)
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })
    
    if petsit_request.response is None:
        petsit_request.delete()
        return jsonify({
            "status": "success",
            "message": "record deleted"
        })
    else:
        return jsonify({
            "status": "success",
            "message": "record deleted"
        })