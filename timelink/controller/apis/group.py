import os
import requests
from flask import Blueprint, session, request, redirect, url_for
import jwt
import model
import json

group = Blueprint('group', __name__)

channel_access_token = os.environ['LINE_CHANNEL_TOKEN']

def get_group_summary(groupId):
    url = f'https://api.line.me/v2/bot/group/{groupId}/summary'
    headers = {'Authorization': "Bearer "+channel_access_token}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 400:
            return {"data": None}
        return {"data": json.loads(resp.text)}
    except Exception:
        return None

@group.route("/groups", methods=["POST"])
def link_group():
    try:
        data = request.get_json()
        groupId = data["data"]["groupId"]
        usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
        user_id = usertoken["id"]
            
        group_summary = get_group_summary(groupId)
        
        if group_summary["data"]:
            group_name = group_summary["data"]["groupName"]
            resp = model.group.create(groupId=groupId, name=group_name, user_id=user_id)
            return {"ok": True, "message": "Linking Successful."}, 200
        return {"error": True, "message": "Linking failed."}, 400
    except Exception as e:
        return {'error': True, "message": "Server Error."}, 500

@group.route("/groups", methods=["GET"])
def get_groups():
    try:
        usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
        user_id = usertoken["id"]
        
        resp = model.group.get_all_by_user(user_id=user_id)
        
        return resp
    except Exception as e:
        return {'error': True, "message": "Server Error."}, 500