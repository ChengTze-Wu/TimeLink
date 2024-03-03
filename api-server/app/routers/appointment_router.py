import json
from flask import Blueprint, request, abort
from app.services import AppointmentService
from app.utils.validators.request_vaildator import RequestValidator
from app.views.response_view import RESTfulResponse
from werkzeug.exceptions import HTTPException
from requests.exceptions import RequestException
from app.utils.validators.token_validator import verify_access_token
from app.utils.converter import decamelize
from app.utils.handlers.jwt_handler import JWTHandler


bp = Blueprint("appointment_router", __name__)
appointment_service = AppointmentService()
jwt_handler = JWTHandler()


@bp.route("", methods=["POST"])
@verify_access_token(access_roles=["liff"])
def create_endpoint():
    try:
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
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        created_appointment = appointment_service.create_one(appointment_json_data, jwt_payload)
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
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        appointment = appointment_service.get_one(appointment_id, jwt_payload)
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
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        line_user_id = request.args.get("line_user_id", None, type=str)
        query = request.args.get("query", None, type=str)

        sort_field = decamelize(request.args.get("sortField", None, type=str))
        sort_order = decamelize(request.args.get("sortOrder", None, type=str))
        filters = decamelize(request.args.get("filters", None, type=str))

        if filters:
            filters: dict = json.loads(filters)
        
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))

        appointments_dataset, total_items_count = appointment_service.get_all(
            page=page,
            per_page=per_page,
            line_user_id=line_user_id,
            sort_field=sort_field,
            sort_order=sort_order,
            query=query,
            with_total_count=True,
            payload=jwt_payload,
        )
        return RESTfulResponse(
            data=appointments_dataset, pagination=(page, per_page, total_items_count)
        ).to_serializable()
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
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        updated_appointment = appointment_service.update_one(
            appointment_id, appointment_json_data, payload=jwt_payload
        )
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
        line_user_id = request.args.get("line_user_id", None, type=str)
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        appointment_service.cancel_one(
            appointment_id=appointment_id, line_user_id=line_user_id, payload=jwt_payload
        )
        return RESTfulResponse().to_serializable(), 204
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)
