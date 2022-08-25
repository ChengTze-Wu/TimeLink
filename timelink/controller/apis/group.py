import requests
from flask import Blueprint, session, request, current_app
import jwt
from timelink import model
import json

bp = Blueprint('group', __name__, url_prefix='/api')

SECRET_KEY = current_app.config['SECRET_KEY']

def get_group_summary(groupId): 
    channel_access_token = current_app.config['LINE_CHANNEL_TOKEN']
    url = f'https://api.line.me/v2/bot/group/{groupId}/summary'
    headers = {'Authorization': "Bearer "+channel_access_token}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 400:
            return {"data": None}
        return {"data": json.loads(resp.text)}
    except Exception:
        return None

@bp.route("/groups", methods=["POST"])
def create():
    try:
        data = request.get_json()
        groupId = data["data"]["groupId"]
        usertoken = jwt.decode(session.get('usertoken'), SECRET_KEY, algorithms=["HS256"])
        user_id = usertoken["id"]

        group_summary = get_group_summary(groupId)

        if group_summary["data"]:
            group_name = group_summary["data"]["groupName"]
            resp = model.group.create(groupId=groupId, name=group_name, user_id=user_id)
            return {"ok": True, "message": "Linking Successful."}, 200
        return {"error": True, "message": "Linking failed."}, 400
    except Exception as e:
        return {'error': True, "message": "Server Error."}, 500

@bp.route("/groups", methods=["GET"])
def get():
    try:
        usertoken = jwt.decode(session.get('usertoken'), SECRET_KEY, algorithms=["HS256"])
        user_id = usertoken["id"]

        data = model.group.get_all_by_user(user_id=user_id)
        
        return {"data": data}, 200
    except Exception as e:
        return {'error': True, "message": "Server Error."}, 500