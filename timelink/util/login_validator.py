from functools import wraps
from flask import session, redirect, url_for
import jwt
from timelink.model import user

def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if session.get('usertoken'):
            usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
            username = usertoken["username"]
        else:
            username = ""
        resp = user.auth(username=username)
        if resp["data"] is None:
            return redirect(url_for('home.index'))
        return func(*args, **kwargs)
    return decorated
