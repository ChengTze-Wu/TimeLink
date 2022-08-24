import secrets
from flask import (
    Blueprint, request, session, make_response
)
import datetime
from timelink import model
import jwt


bp = Blueprint('reserve', __name__, url_prefix='/api')


@bp.route("/reserves" , methods=["POST"])
def create():
    try:
        data = request.get_json()
        bookedDateTime = datetime.datetime.strptime(f"{data['booking_date']} {data['booking_time']}", "%Y-%m-%d %H:%M:%S")
        
        member_id = model.member.get_member_id_by_userId(data["userId"])
        resp = model.reserve.create(service_id=data["service_id"], 
                                    member_id=member_id, 
                                    bookedDateTime=bookedDateTime)
        return resp
    except Exception as e:
        return {'message':str(e)}, 500


@bp.route("/reserves", methods=["GET"])
def get():
    try:
        query_string = request.args.to_dict()
        
        resp = {"data": None}
        
        if "service_id" in query_string and "booking_date" in query_string:
            resp = model.reserve.get_available_time(service_id=query_string["service_id"], 
                                                    booking_date=query_string["booking_date"]) 
        elif "group_id" in query_string:
            usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
            user_id = usertoken["id"]
            resp = model.reserve.get_reserve_by_user_id_and_group_id(user_id=user_id, 
                                                                     group_id=query_string["group_id"])

        return resp
    except Exception as e:
        return {'message':str(e)}, 500
    
@bp.route("/reserves/<int:id>", methods=["DELETE"])
def delete(id):
    try:
        model.reserve.delete_by_id(reserve_id=id)

        return {"ok": True}, 200,
    except Exception as e:
        return {'message':str(e)}, 500