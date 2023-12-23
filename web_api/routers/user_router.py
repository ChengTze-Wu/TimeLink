from flask import Blueprint, request, abort
from web_api.validators.request_vaildator import RequestValidator
from web_api.validators.field_validators import EmailValidator, PasswordValidator
from web_api.views.response_view import RESTfulResponse
from web_api.services.user_service import UserService
from werkzeug.exceptions import HTTPException


bp = Blueprint("user_router", __name__)
user_service = UserService()


@bp.route("", methods=["POST"])
def register_endpoint():
    try:
        request_validator = RequestValidator(
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
            }
        )
        request_validator.check(request)

        user_json_data = request.get_json()
        created_user_data = user_service.create_one(user_json_data)
        return RESTfulResponse(created_user_data, hide_fields=["password"]).to_serializable(), 201
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:user_id>", methods=["DELETE"])
def delete_endpoint(user_id):
    try:
        deleted_user_data = user_service.delete_one(user_id)
        return RESTfulResponse(deleted_user_data, hide_fields=["password"]).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:user_id>", methods=["PUT"])
def update_endpoint(user_id):
    try:
        request_validator = RequestValidator(
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
            }
        )
        request_validator.check(request)

        user_json_data = request.get_json()
        updated_user_data = user_service.update_one(user_id, user_json_data)
        return RESTfulResponse(updated_user_data, hide_fields=["password"]).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:user_id>", methods=["GET"])
def get_one_endpoint(user_id):
    try:
        user_data = user_service.get_one(user_id)
        return RESTfulResponse(user_data, hide_fields=["password"]).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("", methods=["GET"])
def get_all_endpoint():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        query = request.args.get("query", None, type=str)
        status = request.args.get("status", None, type=int)
        user_dataset, total_items_count = user_service.get_all(page=page, per_page=per_page, query=query, status=status, with_total_items=True)
        return RESTfulResponse(
                    user_dataset, 
                    hide_fields=["password", "is_deleted"], 
                    pagination=(page, per_page, total_items_count)
                ).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)