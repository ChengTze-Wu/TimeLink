from flask import Blueprint, request, session
from timelink import model
import jwt


bp = Blueprint('service', __name__, url_prefix='/api')


@bp.route("/services", methods=["POST"])
def add_service():
    try:
        data = request.get_json()
        name = data["name"]
        price = data["price"]
        type = data["type"]
        group_id = data["group_id"]
        openTime = data["openTime"]
        closeTime = data["closeTime"]

        usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
        user_id = usertoken["id"]
        
        resp = model.service.create(name=name, type=type, price=price, group_id=group_id, user_id=user_id, open_time=openTime, close_time=closeTime)
        return resp
    except Exception as e:
        return {'error':str(e)}, 405
    
@bp.route("/services", methods=["GET"])
def get_services():
    try:
        queryString = request.args
        if "groupId" in queryString:
            resp = model.service.get_all_by_groupId(groupId=queryString["groupId"])
        elif "group_id" in queryString:
            resp = model.service.get_all_by_group_id(group_id=queryString["group_id"])
        else:
            usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
            user_id = usertoken["id"]
            resp = model.service.get_all_by_user_id(user_id=user_id)
        return resp
    except Exception as e:
        return {'error':str(e)}, 405
    
@bp.route("/services/<service_id>", methods=["GET"])
def get_service(service_id):
    try:
        resp = model.service.get_all_by_service_id(service_id=service_id)
        return resp
    except Exception as e:
        return {'error':str(e)}, 405
    
@bp.route("/services/<service_id>", methods=["DELETE"])
def delete_service(service_id):
    try:
        resp = model.service.delete(service_id=service_id)
        return resp
    except Exception as e:
        return {'error': str(e)}, 405