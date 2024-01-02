'''
Author: Tze
Date: 2023-12-28
Contact: chengtzewu@gmail.com
'''
from functools import wraps
from flask import current_app, request
from werkzeug.exceptions import Forbidden, Unauthorized, InternalServerError, HTTPException
from web_api.db.models import RoleName
import re
import jwt


def verify_access_token(access_roles: list=None, check_owner=False):
    '''
    Decorator for verifying jwt access token in HTTP Authorization Header Authorization with Bearer prefix.
        > Authorization: Bearer <JWT token>

    Basic Usage: only verify access token
    >>> @app.route("/api/users", methods=["GET"])
    >>> @verify_access_token
    >>> def get_users():
    >>>     pass
       
    Parameters Usage: verify access token and check access roles
    >>> @app.route("/api/users", methods=["GET"])
    >>> @verify_access_token(access_roles=["group_owner", "group_member"])
    >>> def get_all_users():
    >>>    pass

    Owner Usage: verify access token and check owner
    >>> @app.route("/api/users/<uuid:user_id>", methods=["GET"])
    >>> @verify_access_token(check_owner=True)
    >>> def get_user(user_id):
    >>>    pass
    '''
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                jwt_token_with_bearer = request.headers.get('Authorization')
                if not jwt_token_with_bearer:
                    raise Unauthorized("JWT is required")

                jwt_token = re.sub(r'^Bearer ', '', jwt_token_with_bearer)
                payload = jwt.decode(jwt_token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])

                payload_role = payload.get("role")

                if payload_role is RoleName.ADMIN.value:
                    return func(*args, **kwargs)

                if access_roles and 'role' in payload:
                    if payload_role not in access_roles:
                        raise Forbidden("Access denied")

                if check_owner and 'user_id' in kwargs:
                    if payload.get("id") != str(kwargs.get("user_id")):
                        raise Forbidden("Access denied")

            except jwt.ExpiredSignatureError:
                raise Unauthorized("JWT is expired")
            except jwt.InvalidTokenError:
                raise Unauthorized("JWT is invalid")
            except HTTPException as e:
                raise e
            except Exception as e:
                raise InternalServerError(e)

            return func(*args, **kwargs)
        return decorated_function
    return decorator
