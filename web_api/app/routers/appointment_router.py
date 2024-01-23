from flask import Blueprint, request, abort, current_app
from app.services.appointment_service import AppointmentService
from app.utils.validators.request_vaildator import RequestValidator
from app.views.response_view import RESTfulResponse
from werkzeug.exceptions import HTTPException
from requests.exceptions import RequestException
from app.utils.validators.token_validator import verify_access_token
import jwt

bp = Blueprint("appointment_router", __name__)
appointment_service = AppointmentService()

@bp.route("", methods=["POST"], endpoint='create_endpoint')
@verify_access_token(access_roles=['admin', 'user'])
def create_endpoint():
    try:
        request_validator = RequestValidator(
            request_type="json",
            required_fields=["service_id", "reserved_at"],
            field_types={
                "service_id": str,
                "reserved_at": str,
            },
        )
        request_validator.check(request)
        appointment_json_data = request.get_json()

        jwt_token_with_bearer = request.headers.get('Authorization')
        jwt_token = jwt_token_with_bearer.replace("Bearer ", "")
        payload = jwt.decode(jwt_token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        user_id = payload.get("sub")

        created_appointment = appointment_service.create_one(user_id, appointment_json_data)
        return RESTfulResponse(created_appointment).to_serializable(), 201
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:appointment_id>", methods=["PUT"], endpoint='update_endpoint')
@verify_access_token
def update_endpoint(appointment_id):
    try: 
        pass
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:appointment_id>", methods=["DELETE"], endpoint='cancel_endpoint')
@verify_access_token
def cancel_endpoint(appointment_id):
    try:
        pass
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)