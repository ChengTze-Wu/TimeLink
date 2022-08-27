from flask import (
    Blueprint, request, session, current_app
)
import datetime
from timelink import model
import jwt


bp = Blueprint('reserve', __name__, url_prefix='/api')


SECRET_KEY = current_app.config['SECRET_KEY']


@bp.route("/reserves" , methods=["POST"])
def create():
    created_status = False
    try:
        data = request.form.to_dict()

        bookedDateTime = datetime.datetime.strptime(f"{data['select_date_value']} {data['booking_time']}", "%Y-%m-%d %H:%M:%S")
        
        member_id = model.member.get_member_id_by_userId(data["userId"])
        
        if member_id:
            created_status = model.reserve.create(service_id=data["service_id"], 
                                    member_id=member_id, 
                                    bookedDateTime=bookedDateTime)
        if created_status:
            return {"success": True}, 201
        return {"success": False, "error":{"code": 200, "message":"Create Failed"}}, 200
    except Exception as e:
        return {"success": False, "error":{"code": 500, "message": str(e)}}, 500


@bp.route("/reserves", methods=["GET"])
def get():
    dbData = None
    try:
        query_string = request.args.to_dict()
        
        if "service_id" in query_string and "booking_date" in query_string:
            dbData = model.reserve.get_available_time(service_id=query_string["service_id"], 
                                                    booking_date=query_string["booking_date"]) 
            if dbData:
                return {"success": True, "data": dbData}, 200
        elif "group_id" in query_string:
            usertoken = jwt.decode(session.get('usertoken'), SECRET_KEY, algorithms=["HS256"])
            user_id = usertoken["id"]
            dbData = model.reserve.get_reserve_by_user_id_and_group_id(user_id=user_id, 
                                                                     group_id=query_string["group_id"])
            if dbData:
                return {"success": True, "group_id": dbData["group_id"], 
                        "group_name": dbData["group_name"] ,"data": dbData["data"]}, 200
        return {"success": False, "data": None}, 200
    except jwt.exceptions.PyJWTError:
        return {"success": False, "error":{"code": 401, "message":"Unauthorized"}}, 401
    except Exception as e:
        return {"success": False, "error":{"code": 500, "message": str(e)}}, 500
    
@bp.route("/reserves/<int:id>", methods=["DELETE"])
def delete(id):
    try:
        jwt.decode(session.get('usertoken'), SECRET_KEY, algorithms=["HS256"])
        model.reserve.delete_by_id(reserve_id=id)
        return {"success": True}, 200
    except jwt.exceptions.PyJWTError:
        return {"success": False, "error":{"code": 401, "message":"Unauthorized"}}, 401
    except Exception as e:
        return {"success": False, "error":{"code": 500, "message": str(e)}}, 500