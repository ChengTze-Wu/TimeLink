from functools import wraps
from flask import session, redirect, url_for
import jwt
import model

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('usertoken'):
            usertoken = jwt.decode(session.get('usertoken'), "secret", algorithms=["HS256"])
            username = usertoken["username"]
        else:
            username = ""
        resp = model.user.verify(username=username)
        if resp["data"] is None:
            return redirect(url_for('pages.signin'))
        return func(*args, **kwargs)
    return decorated_function