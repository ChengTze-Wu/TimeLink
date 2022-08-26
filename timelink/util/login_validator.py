from functools import wraps
from flask import session, redirect, url_for, current_app
import jwt
from timelink import model

SECRET_KEY = current_app.config['SECRET_KEY']

def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if session.get('usertoken'):
            try:
                usertoken = jwt.decode(session.get('usertoken'), SECRET_KEY, algorithms=["HS256"])
            except jwt.exceptions.ExpiredSignatureError or jwt.exceptions.InvalidSignatureError:
                session.pop('usertoken', None)
                return redirect(url_for('home.index'))
            username = usertoken["username"]
        else:
            username = ""
        dbData = model.user.auth(username=username)
        if not dbData:
            return redirect(url_for('home.index'))
        return func(*args, **kwargs)
    return decorated
