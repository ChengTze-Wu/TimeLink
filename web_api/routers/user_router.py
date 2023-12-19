from flask import Blueprint, request, abort
from web_api.utils.validators import RequestValidator, EmailValidator, PasswordValidator
from web_api.views.response_view import RESTfulResponse
from web_api.services import user_service


bp = Blueprint("user_router", __name__)


@bp.route("", methods=["POST"])
def register_endpoint():
    request_validator = RequestValidator(request)
    request_validator.config(
        request_type="json",
        required_fields=["email", "username", "password", "name"],
        field_types={
            "id": str,
            "email": str,
            "username": str,
            "password": str,
            "name": str,
            "phone": str,
            "is_active": bool,
            "is_deleted": bool,
        },
        field_max_lengths={
            "email": 100,
            "username": 50,
            "password": 100,
            "name": 50,
            "phone": 50,
        },
        field_validators={
            "email": EmailValidator,
            "password": PasswordValidator,
        },
    )
    is_valid = request_validator.check()
    if not is_valid:
        abort(400, request_validator.message)

    user_json_data = request.get_json()
    created_user_data = user_service.create_one(user_json_data)
    return RESTfulResponse(created_user_data, hide_fields=["password"]).to_serializable(), 201


@bp.route("/<user_id>", methods=["DELETE"])
def delete_endpoint(user_id):
    deleted_user_data = user_service.logical_delete_by_id(user_id)
    return RESTfulResponse(deleted_user_data, hide_fields=["password"]).to_serializable()


@bp.route("/<user_id>", methods=["PUT"])
def update_endpoint(user_id):
    request_validator = RequestValidator(request)
    request_validator.config(
        request_type="json",
        field_types={
            "email": str,
            "username": str,
            "password": str,
            "name": str,
            "phone": str,
            "is_active": bool,
            "is_deleted": bool,
        },
        field_max_lengths={
            "email": 100,
            "username": 50,
            "password": 100,
            "name": 50,
            "phone": 50,
        },
        field_validators={
            "email": EmailValidator,
            "password": PasswordValidator,
        },
    )
    is_valid = request_validator.check()
    if not is_valid:
        abort(400, request_validator.message)

    user_json_data = request.get_json()
    updated_user_data = user_service.update_one_by_id(user_json_data, user_id)
    return RESTfulResponse(updated_user_data, hide_fields=["password"]).to_serializable()


@bp.route("/<user_id>", methods=["GET"])
def get_one_endpoint(user_id):
    user_data = user_service.get_one_by_id(user_id)
    return RESTfulResponse(user_data, hide_fields=["password"]).to_serializable()


@bp.route("", methods=["GET"])
def get_all_endpoint():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    query = request.args.get("query", None, type=str)
    status = request.args.get("status", None, type=int)
    user_dataset, total_items_count = user_service.get_all_available_by_filter(page=page, per_page=per_page, query=query, status=status, with_total_items=True)
    return RESTfulResponse(
                user_dataset, 
                hide_fields=["password", "is_deleted"], 
                pagination=(page, per_page, total_items_count)
            ).to_serializable()
