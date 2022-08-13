from flask import Blueprint, request
import datetime
from timelink import model

bp = Blueprint('reserve', __name__, url_prefix='/api')

@bp.route("/reserves" , methods=["POST"])
def create_reserve():
    try:
        data = request.get_json()
        bookedDateTime = datetime.datetime.strptime(f"{data['booking_date']} {data['booking_time']}", "%Y-%m-%d %H:%M:%S")
        
        member_id = model.member.get_member_id_by_userId(data["userId"])
        resp = model.reserve.create(service_id=data["service_id"], 
                                    member_id=member_id, 
                                    bookedDateTime=bookedDateTime)
        return resp
    except Exception as e:
        return {'error':str(e)}, 500


@bp.route("/reserves", methods=["GET"])
def get_reserves():
    try:
        query_string = request.args
        if query_string["service_id"] and query_string["booking_date"]:
            resp = model.reserve.get_available_time(service_id=query_string["service_id"], 
                                                    booking_date=query_string["booking_date"])
        return resp
    except Exception as e:
        return {'error':str(e)}, 500