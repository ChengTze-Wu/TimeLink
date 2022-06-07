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
        return resp.text
    except Exception:
        return None

@group.route("/link", methods=["POST"])
def link():
    try:
        name = request.form["name"]
        groupId = request.form["groupId"]
        usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
        user_id = usertoken["id"]
        
        group_summary = get_group_summary(groupId)
        group_summary = json.loads(group_summary)
        
        if group_summary["groupName"] == name:
            resp = model.group.create(groupId=groupId, name=name, user_id=user_id)
        return redirect(url_for('pages.group'))
    except Exception as e:
        return redirect(url_for('pages.group'))

@group.route("/groups", methods=["GET"])
def get_groups():
    try:
        usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
        user_id = usertoken["id"]
        
        resp = model.group.get_all_by_user(user_id=user_id)
        
        return resp
    except Exception as e:
        return {'error': str(e)}, 405