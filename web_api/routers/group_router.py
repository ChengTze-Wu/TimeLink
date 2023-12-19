from flask import Blueprint, request, abort
from web_api.utils.validators import RequestValidator
from web_api.views.response_view import RESTfulResponse
from web_api.services import group_service


bp = Blueprint("group_router", __name__)


@bp.route("", methods=["POST"])
def create_endpoint():
    request_validator = RequestValidator(request)
    request_validator.config(
        request_type="json",
        required_fields=["name"],
        field_types={
            "name": str,
            "line_group_id": str,
            "is_active": bool,
        },
        field_max_lengths={
            "name": 100,
            "line_group_id": 100,
        },
    )
    is_valid = request_validator.check()
    if not is_valid:
        abort(400, request_validator.message)

    group_json_data = request.get_json()
    created_group_data = group_service.create_one(group_json_data)
    return RESTfulResponse(created_group_data).to_serializable(), 201


@bp.route("/<group_id>", methods=["PUT"])
def update_endpoint(group_id):
    request_validator = RequestValidator(request)
    request_validator.config(
        request_type="json",
        field_types={
            "name": str,
            "line_group_id": str,
            "is_active": bool,
        },
        field_max_lengths={
            "name": 100,
            "line_group_id": 100,
        },
    )
    is_valid = request_validator.check()
    if not is_valid:
        abort(400, request_validator.message)

    group_json_data = request.get_json()
    updated_group_data = group_service.update_one_by_id(group_json_data, group_id)
    return RESTfulResponse(updated_group_data).to_serializable()


@bp.route("/<group_id>", methods=["DELETE"])
def delete_endpoint(group_id):
    deleted_group_data = group_service.logical_delete_by_id(group_id)
    return RESTfulResponse(deleted_group_data).to_serializable()


@bp.route("/<group_id>", methods=["GET"])
def get_one_endpoint(group_id):
    group_data = group_service.get_one_by_id(group_id)
    return RESTfulResponse(group_data).to_serializable()


@bp.route("", methods=["GET"])
def get_all_endpoint():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    query = request.args.get("query", None, type=str)
    status = request.args.get("status", None, type=int)
    groups_data = group_service.get_all_available_by_filter(
        page=page,
        per_page=per_page,
        query=query,
        status=status,
        with_total_items=True,
    )
    return RESTfulResponse(groups_data).to_serializable()