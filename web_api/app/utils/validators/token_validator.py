'''
Author: Tze
Date: 2023-12-28
Contact: chengtzewu@gmail.com
'''
from functools import wraps, partial
from werkzeug.exceptions import Forbidden, InternalServerError, HTTPException, BadRequest
from app.db.models import RoleName
from app.services.token_service import JWTService

def verify_access_token(func=None, *, access_roles: list=None, check_owner=False):
    '''
    Decorator for verifying jwt access token in HTTP Authorization Header Authorization with Bearer prefix.
        > Authorization: Bearer <JWT token>

    If the JWT role is 'admin', it will pass all verifications.

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
    if func is None:
        return partial(verify_access_token, access_roles=access_roles, check_owner=check_owner)

    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            payload = JWTService().get_payload()

            if not payload:
                raise BadRequest("Missing access token")

            payload_role = payload.get("role")

            if payload_role == RoleName.ADMIN.value:
                return func(*args, **kwargs)

            if access_roles and 'role' in payload:
                if payload_role not in access_roles:
                    raise Forbidden("Access denied, role is not allowed.")

            if check_owner and 'user_id' in kwargs:
                if payload.get("sub") != str(kwargs.get("user_id")):
                    raise Forbidden("Access denied, user is not owner.")

        except HTTPException as e:
            raise e
        except Exception as e:
            raise InternalServerError(e)

        return func(*args, **kwargs)
    return decorated_function
