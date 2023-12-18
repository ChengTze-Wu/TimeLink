from flask import Blueprint, request, abort
from web_api.utils.validators import RequestValidator, EmailValidator, PasswordValidator
from web_api.views.response_view import RESTfulResponse
from web_api.services import account_service


bp = Blueprint("user_router", __name__)


@bp.route("", methods=["POST"])
def register():
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
    user = account_service.create_one(user_json_data)
    return RESTfulResponse(user, hide_fields=["password"]).to_serializable(), 201


@bp.route("/<uuid>", methods=["DELETE"])
def delete(uuid):
    user = account_service.logical_delete(uuid)
    return RESTfulResponse(user, hide_fields=["password"]).to_serializable()


@bp.route("/<uuid>", methods=["PUT"])
def update(uuid):
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
    user = account_service.update_one(user_json_data, uuid)
    return RESTfulResponse(user, hide_fields=["password"]).to_serializable()


@bp.route("/<username>", methods=["GET"])
def get_one(username):
    user = account_service.get_one(username)
    return RESTfulResponse(user, hide_fields=["password"]).to_serializable()


@bp.route("", methods=["GET"])
def get_all():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    query = request.args.get("query", None, type=str)
    status = request.args.get("status", None, type=int)
    users, total_available_users = account_service.get_all_available_by_pagination(page=page, per_page=per_page, query=query, status=status, with_total_items=True)
    return RESTfulResponse(
                users, 
                hide_fields=["password", "is_deleted"], 
                pagination=(page, per_page, total_available_users)
            ).to_serializable()
