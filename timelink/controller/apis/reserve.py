from flask import Blueprint, request
import model

reserve = Blueprint('reserve', __name__)

@reserve.route("/reserve" , methods=["GET"])
def get_reserves():
    # return {'results':[{'id':'u0001', 'name':'晨晨', 'serve_name':'剪髮', 'date':'2022-5-18', 'time':'15:00'}]}
    return {'error':True}, 405