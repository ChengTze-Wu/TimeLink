from flask import Blueprint, request, abort
from web_api.services import user_service
from web_api.validators.request_vaildator import RequestValidator
from web_api.validators.field_validators import PasswordValidator
from web_api.views.response_view import RESTfulResponse


bp = Blueprint("auth_router", __name__)


@bp.route("/", methods=["POST"])
def authenticate_endpoint():
    request_validator = RequestValidator(
        request_type="form",
        required_fields=["username", "password"],
        field_types={"username": str, "password": str},
        field_max_lengths={"username": 100, "password": 100},
        field_validators={"password": PasswordValidator}
    )
    request_validator.check(request)

    username = request.form.get("username")
    password = request.form.get("password")

    # jwt_token = user_service.login(username, password)

    return RESTfulResponse({"token": "jwt_token"}).to_serializable()
