from flask import Blueprint, request, session, redirect, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
import model
import jwt
from util import login_required


user = Blueprint('user', __name__)

@user.route("/signin", methods=["POST"])
def signin():
    try:
        username = request.form["username"]
        password = request.form["password"]
        resp = model.user.verify(username)
        if resp["data"]:
            query_password = resp["data"]["password"]
            usertoken = {"id":resp["data"]["id"], "username":resp["data"]["username"]}
        if query_password == password:
            session["usertoken"] = jwt.encode(usertoken, "secret", algorithm="HS256")
            return redirect(url_for("pages.index"))
        return {'error': "登入失敗"}
    except Exception as e:
        return {'error': str(e)}, 405

@user.route("/signup", methods=["POST"])
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
            return redirect(url_for("pages.signin"))
        else:
            return {"error": True}
    except Exception as e:
        return {'error': str(e)}, 405
    
@user.route('/signout', methods=["GET"])
def signout():
    session.pop('usertoken', None)
    return redirect(url_for('pages.signin'))
