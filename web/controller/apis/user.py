from flask import Blueprint, request, session, current_app
from web import model
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

bp = Blueprint('user', __name__, url_prefix='/api')

SECRET_KEY = current_app.config['SECRET_KEY']

# Login / Logout
@bp.route("/auth", methods=["POST"])
def login():
    try:
        data = request.form.to_dict()
        username = data["username"]
        password = data["password"]
        dbData = model.user.auth(username)
        if dbData:
            hashed_password = dbData["password"]
            if check_password_hash(hashed_password, password):
               
                usertoken = {"id": dbData["id"], "username": dbData["username"], 
                             "exp":datetime.datetime.utcnow() + datetime.timedelta(hours=24)}
                session["usertoken"] = jwt.encode(usertoken, SECRET_KEY, algorithm="HS256")
                session.permanent = True

                return {"success": True}, 201  # session created
        return {'success': False, "error": {"code": 400, "message": "Login Failed"}}, 400
    except Exception as e:
        return {'success': False, "error": {"code": 500, "message": str(e)}}, 500
    
@bp.route('/auth', methods=["DELETE"])
def logout():
    try:
        session.pop('usertoken', None)
        return {"success": True}, 200
    except Exception as e:
        return {"success": False, "error":{"code": 500, "message": str(e)}}, 500


@bp.route("/user", methods=["POST"])
def signup():
    try:
        data = request.form.to_dict()
        username = data["username"]
        password = data["password"]
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        
        hashed_password = generate_password_hash(password)
        
        created_status = model.user.create(username=username, password=hashed_password, name=name, email=email, phone=phone)
        if created_status:
            return {"success": True}, 201
        return {"success": False, "error":{"code": 400, "message":"Create Failed"}}, 400
    except Exception as e:
        return {"success": False, "error":{"code": 500, "message": str(e)}}, 500
    

@bp.route("/user", methods=["GET"])
def get():
    try:
        usertoken = jwt.decode(session.get('usertoken'), SECRET_KEY, algorithms=["HS256"])
        username = usertoken["username"]
        user_id = usertoken["id"]
        return {"success": True ,"data": {"username": username, "user_id": user_id}}, 200
    except jwt.exceptions.PyJWTError:
        return {"success": False, "error":{"code": 401, "message":"Unauthorized"}}, 401
    except Exception as e:
        return {"success": False, "error":{"code": 500, "message": str(e)}}, 500