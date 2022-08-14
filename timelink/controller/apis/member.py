from flask import Blueprint, session, request
import jwt
from timelink import model

bp = Blueprint('member', __name__, url_prefix='/api')

# usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
# user_id = usertoken["id"]

