from functools import wraps
from web_api.db.models import User
import jwt
from flask import session, redirect, url_for, current_app
def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if session.get('usertoken'):
            try:
                usertoken = jwt.decode(session.get('usertoken'), current_app.config['SECRET_KEY'], algorithms=["HS256"])
            except jwt.exceptions.ExpiredSignatureError or jwt.exceptions.InvalidSignatureError:
                session.pop('usertoken', None)
                return redirect(url_for('home.index'))
            username = usertoken["username"]
        else:
            username = ""
        dbData = User.query.filter_by(username=username).first()
        if not dbData:
            return redirect(url_for('home.index'))
        return func(*args, **kwargs)
    return decorated
