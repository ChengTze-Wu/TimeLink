from flask import Blueprint, request, session
import model
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


user = Blueprint('user', __name__)


# Login / Logout
@user.route("/auth", methods=["POST"])
def login():
    try:
        request_json = request.get_json()
        username = request_json["username"]
        password = request_json["password"]
        resp = model.user.auth(username)
        if resp["data"]:
            hashed_password = resp["data"]["password"]
            if check_password_hash(hashed_password, password):
                usertoken = {"id":resp["data"]["id"], "username":resp["data"]["username"]}
                session["usertoken"] = jwt.encode(usertoken, "secret", algorithm="HS256")
                return {"ok": True, "message": "Login Successful."}, 200
        return {'error': True, "message": "Login failed."}, 400
    except Exception as e:
        return {'error': True, "message": "Server Error."}, 500
    
@user.route('/auth', methods=["DELETE"])
def logout():
    try:
        session.pop('usertoken', None)
        return {"ok": True, "message": "Logout Successful."}, 200
    except Exception as e:
        return {'error': True, "message": "Server Error."}, 500




@user.route("/user", methods=["POST"])
def signup():
    try:
        request_json = request.get_json()
        username = request_json["username"]
        password = request_json["password"]
        name = request_json["name"]
        email = request_json["email"]
        phone = request_json["phone"]
        
        hashed_password = generate_password_hash(password)
        
        resp = model.user.create(username=username, password=hashed_password, name=name, email=email, phone=phone)
        if resp["data"]:
            return {"ok": True, "message": "Signup Successful."}, 200
        return {"error": True, "message": "Signup failed."}, 400
    except Exception as e:
        return  {'error': True, "message": "Server Error."}, 500
