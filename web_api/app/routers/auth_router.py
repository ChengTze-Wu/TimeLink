from flask import Blueprint, request, abort
from app.services.user_service import UserService
from app.utils.validators.request_vaildator import RequestValidator
from app.utils.validators.field_validators import PasswordValidator
from app.views.response_view import RESTfulResponse
from werkzeug.exceptions import HTTPException
from requests.exceptions import RequestException


bp = Blueprint("auth_router", __name__)
user_service = UserService()


@bp.route("", methods=["POST"])
def auth_endpoint():
    try:
        request_validator = RequestValidator(
                request_type="json",
                required_fields=["username", "password"],
                field_types={"username": str, "password": str},
                field_max_lengths={"username": 100, "password": 100},
                field_validators={"password": PasswordValidator}
            )
        request_validator.check(request)
        credentialsObject = request.get_json()
        auth_result = user_service.auth(credentialsObject)
        return RESTfulResponse(auth_result).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)
