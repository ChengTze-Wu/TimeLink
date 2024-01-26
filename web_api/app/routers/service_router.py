from flask import Blueprint, request, abort
from app.utils.validators.request_vaildator import RequestValidator
from app.views.response_view import RESTfulResponse
from app.services import ServiceService
from werkzeug.exceptions import HTTPException
from app.utils.validators.token_validator import verify_access_token

bp = Blueprint("service_router", __name__)


@bp.route("", methods=["POST"])
@verify_access_token(access_roles=["group_owner"])
def create_endpoint():
    service_service = ServiceService()
    try:
        request_validator = RequestValidator(
            request_type="json",
            required_fields=["name"],
            field_types={
                "name": str,
                "price": int | float,
                "image": str,
                "description": str,
                "working_period": int,
                "is_active": bool,
                "working_hours": list,
                "unavailable_periods": list,
                "groups": list
            },
            field_max_lengths={
                "name": 50,
                "image": 100,
                "description": 100,
            }
        )
        request_validator.check(request)
        service_json_data = request.get_json()
        created_service_data = service_service.create_one(service_json_data)
        return RESTfulResponse(created_service_data).to_serializable(), 201
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:service_id>", methods=["DELETE"])
def delete_endpoint(service_id):
    service_service = ServiceService()
    try:
        deleted_service_data = service_service.delete_one(service_id)
        return RESTfulResponse(deleted_service_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:service_id>", methods=["PUT"])
def update_endpoint(service_id):
    service_service = ServiceService()
    try:
        request_validator = RequestValidator(
            request_type="json",
            field_types={
                "name": str,
                "price": int | float,
                "image": str,
                "description": str,
                "working_period": int,
                "is_active": bool,
                "working_hours": list,
                "unavailable_periods": list,
                "groups": list
            },
            field_max_lengths={
                "name": 50,
                "image": 100,
                "description": 100,
            }
        )
        request_validator.check(request)
        service_json_data = request.get_json()
        updated_service_data = service_service.update_one(service_id, service_json_data)
        return RESTfulResponse(updated_service_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:service_id>", methods=["GET"])
@verify_access_token(access_roles=["admin", "group_owner"])
def get_one_endpoint(service_id):
    service_service = ServiceService()
    try:
        service_data = service_service.get_one(service_id)
        return RESTfulResponse(service_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("", methods=["GET"])
@verify_access_token(access_roles=["admin", "group_owner"])
def get_all_endpoint():
    service_service = ServiceService()
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        query = request.args.get("query", None, type=str)
        status = request.args.get("status", None, type=int)
        service_dataset, total_items_count = service_service.get_all(page=page, per_page=per_page, query=query, status=status, with_total_items=True)
        return RESTfulResponse(service_dataset, pagination=(page, per_page, total_items_count)).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)