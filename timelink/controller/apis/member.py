from flask import Blueprint, session, request, redirect, url_for
import jwt
import model

member = Blueprint('member', __name__)

usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
user_id = usertoken["id"]