from flask import Blueprint, request, session, redirect, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
import model
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
            query_password = resp["data"]["password"]
            usertoken = {"id":resp["data"]["id"], "username":resp["data"]["username"]}
            if query_password == password:
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
        username = request.form["username"]
        # hashed_password = generate_password_hash(request.form["password"])
        password = request.form["password"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        resp = model.user.create(username=username, password=password, name=name, email=email, phone=phone)
        if resp["data"]:
            return redirect(url_for("home.index"))
        else:
            return {"error": True}
    except Exception as e:
        return {'error': str(e)}, 500
