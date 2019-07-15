from flask import Blueprint
from flask import request, jsonify
import json, datetime

from mpn import app#, mongo
from mpn.helper_funcs.helper import token_required, admin_only
from mpn.models import Review, PetReview, UserReview

review_blueprint = Blueprint("review_blueprint", __name__)


@review_blueprint.route("/user/<user_id>/reviews/given/", methods=["GET"])
def get_user_reviews_given(user_id):
    reviews_data = []
    for review in UserReview.objects(reviewer__id = user_id):
        reviews_data.append(json.loads(review.to_json()))
    return jsonify({
        "status": "success",
        "reviews": reviews_data
    })

@review_blueprint.route("/user/<user_id>/reviews/received/", methods=["GET"])
def get_user_reviews_received(user_id):
    reviews_data = []
    for review in UserReview.objects(user__id=user_id):
        reviews_data.append(json.loads(review.to_json()))
    return jsonify({
        "status": "success",
        "reviews": reviews_data
    })

@review_blueprint.route("/pet/<pet_id>/reviews/received", methods=["GET"])
def get_pet_reviews_received(pet_id):
    reviews_data = []
    for review in PetReview.objects(pet__id=pet_id):
        reviews_data.append(json.loads(review.to_json()))
    return jsonify({
        "status": "success",
        "reviews": reviews_data
    })


@review_blueprint.route("/user/review/<review_id>/", methods=["GET"])
def get_user_review(review_id):

    # get review
    try:
        review = UserReview.objects.get(id=review_id)
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })

    # return json 
    return jsonify({
        "status": "success",
        "review": json.loads(review.to_json())
    })


@review_blueprint.route("/pet/review/<review_id>/", methods=["GET"])
def get_pet_review(review_id):

    # get review
    try:
        review = PetReview.objects.get(id=review_id)
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })

    # return json 
    return jsonify({
        "status": "success",
        "review": json.loads(review.to_json())
    })


@review_blueprint.route("/user/review/add/", methods=["POST"])
@token_required
def add_user_review(current_user):

    # get provided data
    data = request.get_json()

    # create and add review
    review = UserReview(
        user = data.get("user_id"),
        reviewer = current_user,
        rating = data.get("rating"),
        comment = data["comment"]
    )
    review.save()

    return jsonify({
        "status": "success",
        "message": "record created",
        "review_id": str(review.id)
    })

@review_blueprint.route("/pet/review/add/", methods=["POST"])
@token_required
def add_pet_review(current_user):

    # get provided data
    data = request.get_json()

    # create and add review
    review = PetReview(
        user = data.get("user_id"),
        reviewer = current_user,
        rating = data.get("rating"),
        comment = data["comment"]
    )
    review.save()

    return jsonify({
        "status": "success",
        "message": "record created",
        "review_id": str(review.id)
    })




def update_review(review, data):

    # update
    review.rating = data.get("rating")
    review.comment = data.get("comment")
    review.updated_timestamp = datetime.datetime.utcnow()
    review.save()

    # return json result
    return jsonify({
        "status": "success",
        "message": "record updated",
        "review_id": str(review.id)
    })

@review_blueprint.route("/user/review/<review_id>/update/", methods=["PUT"])
@token_required
def update_user_review(current_user):

    # get provided data
    data = request.get_json()

    # get review
    try:
        review = UserReview.objects.get(id=review_id, reviewer__id=current_user.id)
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })

    # update
    update_review(review, data)

@review_blueprint.route("/pet/review/<review_id>/update/", methods=["PUT"])
@token_required
def update_pet_review(current_user):

    # get provided data
    data = request.get_json()

    # get review
    try:
        review = PetReview.objects.get(id=review_id, reviewer__id=current_user.id)
    except:
        return jsonify({
            "status": "error",
            "message": "No record found"
        })

    # update
    update_review(review, data)



@review_blueprint.route("/user/review/<review_id>/delete/", methods=["DELETE"])
@token_required
def delete_user_review(current_user, review_id):
    try:
        review = UserReview.object.get(id=review_id, reviewer__id=current_user.id)
    except:
        return jsonify({
            "status": "error",
            "message": "No review found"
        })
    review.delete()
    return jsonify({
        "status": "success",
        "message": "record deleted"
    })

@review_blueprint.route("/pet/review/<review_id>/delete/", methods=["DELETE"])
@token_required
def delete_pet_review(current_user, review_id):
    try:
        review = PetReview.object.get(id=review_id, reviewer__id=current_user.id)
    except:
        return jsonify({
            "status": "error",
            "message": "No review found"
        })
    review.delete()
    return jsonify({
        "status": "success",
        "message": "record deleted"
    })