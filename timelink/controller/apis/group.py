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
            return None
        return json.loads(resp.text)
    except Exception:
        return None

@bp.route("/groups", methods=["POST"])
def create():
    try:
        data = request.form.to_dict()
        groupId = data["groupId"]
        usertoken = jwt.decode(session.get('usertoken'), SECRET_KEY, algorithms=["HS256"])
        user_id = usertoken["id"]

        group_summary = get_group_summary(groupId)

        if group_summary:
            group_name = group_summary["groupName"]
            created_status = model.group.create(groupId=groupId, name=group_name, user_id=user_id)
            if created_status:
                return {"success": True}, 201
        return {"success": False, "error": {"code": 200, "message":"Create Failed"}}, 200
    except jwt.exceptions.PyJWTError:
        return {"success": False, "error": {"code": 401, "message":"Unauthorized"}}, 401
    except Exception as e:
        return {"success": False, "error": {"code": 500, "message": str(e)}}, 500

@bp.route("/groups", methods=["GET"])
def get():
    try:
        usertoken = jwt.decode(session.get('usertoken'), SECRET_KEY, algorithms=["HS256"])
        user_id = usertoken["id"]

        dbData = model.group.get_all_by_user_id(user_id=user_id)
        if dbData:
            return {"success": True, "data": dbData}, 200
        return {"success": False, "data": None}, 200
    except jwt.exceptions.PyJWTError:
        return {"success": False, "error": {"code": 401, "message":"Unauthorized"}}, 401
    except Exception as e:
        return {"success": False, "error": {"code": 500, "message": str(e)}}, 500