from flask import Blueprint, request, abort
from web_api.validators.request_vaildator import RequestValidator
from web_api.views.response_view import RESTfulResponse
from services.appointment_service import AppointmentService
from datetime import datetime
from werkzeug.exceptions import HTTPException


bp = Blueprint("appointment_router", __name__)
appointment_service = AppointmentService()


@bp.route("/appointments", methods=["POST"])
def create_appointment_endpoint():
    try:
        request_validator = RequestValidator(
            request_type="json",
            required_fields=["user_id", "service_id", "appointment_datetime"],
            field_types={
                "user_id": str,
                "service_id": str,
                "appointment_datetime": datetime,
            },
            field_max_lengths={
                "user_id": 100,
                "service_id": 100,
            }
        )
        request_validator.check(request)

        appointment_data = request.get_json()
        created_appointment_data = appointment_service.create_appointment(
            appointment_data["user_id"], 
            appointment_data["service_id"],  
            appointment_data["appointment_datetime"]
        )
        return RESTfulResponse(created_appointment_data).to_serializable(), 201
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)