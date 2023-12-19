from flask import Blueprint, request, abort
from web_api.utils.validators import RequestValidator
from web_api.views.response_view import RESTfulResponse
from web_api.services import service_service


bp = Blueprint("service_router", __name__)


@bp.route("", methods=["POST"])
def create_endpoint():
    request_validator = RequestValidator(request)
    request_validator.config(
        request_type="json",
        required_fields=["name"],
        field_types={
            "name": str,
            "price": int,
            "image": str,
            "period_time": int,
            "open_time": int,
            "close_time": int,
            "start_date": str,
            "end_date": str,
            "is_active": bool,
            "unavailable_periods": list,
        },
        field_max_lengths={
            "name": 100,
            "image": 100,
            "start_date": 100,
            "end_date": 100,
            "unavailable_periods": 100,
        },
    )
    is_valid = request_validator.check()
    if not is_valid:
        abort(400, request_validator.message)

    service_json_data = request.get_json()
    created_service_data = service_service.create_one(service_json_data)
    return RESTfulResponse(created_service_data).to_serializable(), 201


@bp.route("/<service_id>", methods=["DELETE"])
def delete_endpoint(service_id):
    deleted_service_data = service_service.logical_delete_by_id(service_id)
    return RESTfulResponse(deleted_service_data).to_serializable()


@bp.route("/<service_id>", methods=["PUT"])
def update_endpoint(service_id):
    request_validator = RequestValidator(request)
    request_validator.config(
        request_type="json",
        field_types={
            "name": str,
            "price": int,
            "image": str,
            "period_time": int,
            "open_time": int,
            "close_time": int,
            "start_date": str,
            "end_date": str,
            "unavailable_periods": list,
            "is_active": bool,
        },
        field_max_lengths={
            "name": 100,
            "image": 100,
            "start_date": 100,
            "end_date": 100,
            "unavailable_periods": 100,
        },
    )
    is_valid = request_validator.check()
    if not is_valid:
        abort(400, request_validator.message)

    service_json_data = request.get_json()
    updated_service_data = service_service.update_one_by_id(service_id, service_json_data)
    return RESTfulResponse(updated_service_data).to_serializable()


@bp.route("", methods=["GET"])
def get_all_endpoint():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    query = request.args.get("query", None, type=str)
    status = request.args.get("status", None, type=int)
    service_dataset, total_items_count = service_service.get_all_available_by_filter(page=page, per_page=per_page, query=query, status=status)
    return RESTfulResponse(service_dataset, pagination=(page, per_page, total_items_count)).to_serializable()