from flask import Blueprint, request, abort
from app.services import AppointmentService
from app.utils.validators.request_vaildator import RequestValidator
from app.views.response_view import RESTfulResponse
from werkzeug.exceptions import HTTPException
from requests.exceptions import RequestException
from app.utils.validators.token_validator import verify_access_token


bp = Blueprint("appointment_router", __name__)


@bp.route("", methods=["POST"])
@verify_access_token(access_roles=['liff'])
def create_endpoint():
    try:
        appointment_service = AppointmentService()
        request_validator = RequestValidator(
            request_type="json",
            required_fields=["service_id", "reserved_at"],
            field_types={
                "line_user_id": str,
                "service_id": str,
                "reserved_at": str,
                "note": str,
            },
        )
        appointment_json_data = request_validator.process(request)
        created_appointment = appointment_service.create_one(appointment_json_data)
        return RESTfulResponse(created_appointment).to_serializable(), 201
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:appointment_id>", methods=["GET"])
@verify_access_token
def get_one_endpoint(appointment_id):
    try:
        appointment_service = AppointmentService()
        appointment = appointment_service.get_one(appointment_id)
        return RESTfulResponse(appointment).to_serializable(), 200
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)


@bp.route("", methods=["GET"])
@verify_access_token
def get_all_endpoint():
    try:
        appointment_service = AppointmentService()
        line_user_id = request.args.get("line_user_id", None, type=str)
        service_id = request.args.get("service_id", None, type=str)
        appointments_dataset = appointment_service.get_all(line_user_id=line_user_id, service_id=service_id)
        return RESTfulResponse(appointments_dataset).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:appointment_id>", methods=["PUT"])
@verify_access_token
def update_endpoint(appointment_id):
    try:
        appointment_service = AppointmentService()
        request_validator = RequestValidator(
            request_type="json",
            required_fields=["reserved_at"],
            field_types={
                "reserved_at": str,
                "note": str,
                "line_user_id": str,
                "is_active": bool,
            },
        )
        appointment_json_data = request_validator.process(request)
        updated_appointment = appointment_service.update_one(appointment_id, appointment_json_data)
        return RESTfulResponse(updated_appointment).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:appointment_id>", methods=["DELETE"])
@verify_access_token
def cancel_endpoint(appointment_id):
    try:
        appointment_service = AppointmentService()
        line_user_id = request.args.get("line_user_id", None, type=str)
        appointment_service.cancel_one(appointment_id=appointment_id, line_user_id=line_user_id)
        return RESTfulResponse().to_serializable(), 204
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)
