from flask import Blueprint, request, abort, make_response
from web_app.api.services import account_service
from web_app.utils.validators import RequestValidator, PasswordValidator


bp = Blueprint("auth_router", __name__)


@bp.route("/", methods=["GET"])
def login():
    request_validator = RequestValidator(request)
    request_validator.config(
        request_type="form",
        required_fields=["username", "password"],
        field_types={"username": str, "password": str},
        field_max_lengths={"username": 100, "password": 100},
        field_validators={"password": PasswordValidator},
    )
    is_valid = request_validator.check()
    if not is_valid:
        abort(400, request_validator.message)
    
    username = request.form.get("username")
    password = request.form.get("password")

    jwt_token = account_service.login(username, password)

    response = make_response()
    response.set_cookie("usertoken", jwt_token, httponly=True, samesite="Strict", secure=True)
    return response


@bp.route("/", methods=["DELETE"])
def logout():
    response = make_response()
    response.set_cookie("usertoken", "", httponly=True, samesite="Strict", secure=True)
    return response
