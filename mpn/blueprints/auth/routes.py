from flask import Blueprint
from functools import wraps
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from mpn import app#, mongo
from mpn.models import User


auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/login/")
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    # get supplied email address (saved in request authorization username)
    email_address = auth.username

    user = User.objects.get(email_address=email_address)
    if not user:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    # if authenticated with correct password
    if check_password_hash(user.password_hashed, auth.password):
        token = jwt.encode(
            {
                "user_id": str(user.id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10080)
            },
            app.config["SECRET_KEY"]
        )
        return jsonify({
            "token": token.decode("UTF-8")
        })

    return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})
