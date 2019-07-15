from functools import wraps
from flask import request, jsonify
import jwt
from bson.objectid import ObjectId

from mpn import app#, mongo
from mpn.models import User


def admin_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing!"})

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.objects.get(id = data["user_id"])
        except Exception as e:
            print(e)
            return jsonify({"message": "Token is invalid"}), 401

        if not current_user.admin:
            return jsonify({"message": "You're not an admin. Cannot perform that function!"})

        return f(current_user, *args, **kwargs)
    return decorated


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing!"})

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.objects.get(id = data["user_id"])
        except Exception as e:
            print(e)
            return jsonify({"message": "Token is invalid"}), 401

        return f(current_user, *args, **kwargs)
    return decorated




