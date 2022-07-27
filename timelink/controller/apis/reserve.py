from flask import Blueprint, request
import datetime
import model

reserve = Blueprint('reserve', __name__)

@reserve.route("/reserve" , methods=["POST"])
def add_reserve():
    # Service
    # {data: [{id: 1, name: "", type: "", price: "", group_id: "", 
    # open_time: "", close_time: "", not_available_time: ""}]}
    
    # Reserve
    # {data: [{id: 1, service_id: 1, member_id: 1, 
    # start_time: "", end_time: "", status: ""}]}
    
    data = request.get_json()
    start_time = data["start_time"]
    end_time = data["end_time"]
    
    # Service
    service_id = request.args.get("service_id")
    resp = model.service.get_all_by_service_id(service_id)
    data = resp["data"]
    openTime = data[0]["open_time"]
    closeTime = data[0]["close_time"]
    
    # compare
    if start_time < openTime or end_time > closeTime:
        return {'error':'Time is not available'}, 405
    else:
        return {'success':'Time is available'}, 200
    
    print(data)
    return {"ok": "ok"}, 200


