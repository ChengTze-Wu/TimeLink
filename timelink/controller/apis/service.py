from flask import Blueprint, request, session, redirect, url_for
import model
import jwt


service = Blueprint('service', __name__)


@service.route("/service", methods=["POST"])
def add_service():
    try:
        data = request.get_json()
        name = data["name"]
        price = data["price"]
        type = data["type"]
        group_id = data["groupId"]

        usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
        user_id = usertoken["id"]
        
        resp = model.service.create(name=name, type=type, price=price, group_id=group_id, user_id=user_id)
        return resp
    except Exception as e:
        return {'error':str(e)}, 405
    
    
@service.route("/groups_option", methods=["GET"])
def get_groups_option():
    try:
        usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
        user_id = usertoken["id"]
        resp = model.group.get_all_by_user(user_id=user_id)
        return resp
    except Exception as e:
        return {'error':str(e)}, 405
    
@service.route("/services", methods=["GET"])
def get_services():
    try:
        usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
        user_id = usertoken["id"]
        resp = model.service.get_all_by_user_id(user_id=user_id)
        return resp
    except Exception as e:
        return {'error':str(e)}, 405
    
@service.route("/service", methods=["DELETE"])
def delete_service():
    try:
        id = request.get_data(as_text=True)
        resp = model.service.delete(id=id)
        return resp
    except Exception as e:
        return {'error': str(e)}, 405