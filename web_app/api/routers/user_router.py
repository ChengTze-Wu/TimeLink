from flask import Blueprint, request, abort
from web_app.utils.validators import RequestValidator, EmailValidator, PasswordValidator
from web_app.utils.response_handlers import RESTfulResponse
from web_app.api.services import account_service


bp = Blueprint("user_router", __name__)


@bp.route("", methods=["POST"])
def register():
    request_validator = RequestValidator(request)
    request_validator.config(
        request_type="json",
        required_fields=["email", "username", "password", "name"],
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
            "username": 100,
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
    return RESTfulResponse(user, hide_fields=["password"]).to_dict(), 201


@bp.route("/<username>", methods=["DELETE"])
def delete(username):
    user = account_service.logical_delete(username)
    return RESTfulResponse(user, hide_fields=["password"]).to_dict()


@bp.route("/<username>", methods=["PUT"])
def update(username):
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
            "username": 100,
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
    user = account_service.update_one(user_json_data, username)
    return RESTfulResponse(user, hide_fields=["password"]).to_dict()


@bp.route("/<username>", methods=["GET"])
def get_one(username):
    user = account_service.get_one(username)
    return RESTfulResponse(user, hide_fields=["password"]).to_dict()


@bp.route("", methods=["GET"])
def get_all():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    users, total_available_users = account_service.get_all_available_by_pagination(page=page, per_page=per_page, with_total_items=True)
    return RESTfulResponse(
                users, 
                hide_fields=["password", "is_deleted", "is_active"], 
                pagination=(page, per_page, total_available_users)
            ).to_dict()
