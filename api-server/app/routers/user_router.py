from flask import Blueprint, request, abort
from app.utils.validators.request_vaildator import RequestValidator
from app.utils.validators.field_validators import EmailValidator, PasswordValidator
from app.utils.validators.token_validator import verify_access_token
from app.views.response_view import RESTfulResponse
from app.services import UserService, AppointmentService
from werkzeug.exceptions import HTTPException
from app.utils.handlers.jwt_handler import JWTHandler


bp = Blueprint("user_router", __name__)
user_service = UserService()
appintment_service = AppointmentService()
jwt_handler = JWTHandler()


@bp.route("", methods=["POST"])
def register_endpoint():
    try:
        request_validator = RequestValidator(
            request_type="json",
            required_fields=["email", "username", "password", "name"],
            field_types={
                "email": str,
                "username": str,
                "password": str,
                "name": str,
                "phone": str,
                "line_user_id": str,
                "is_active": bool,
                "role": str,
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
        request_validator.check(request)
        user_json_data = request.get_json()
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        created_user_data = user_service.create_one(user_json_data, payload=jwt_payload)
        return (
            RESTfulResponse(
                created_user_data
            ).to_serializable(),
            201,
        )
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:user_id>", methods=["GET"])
@verify_access_token(check_owner=True)
def get_one_endpoint(user_id):
    try:
        user_data = user_service.get_one(user_id=user_id)
        return RESTfulResponse(user_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<line_user_id>/appointments", methods=["GET"])
@verify_access_token(access_roles=["line_bot"])
def get_appintments_endpoint(line_user_id):
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        coming = request.args.get("coming", None, type=bool)
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))

        if coming is not None:
            appintments = appintment_service.get_the_most_coming_appointment(
                line_user_id=line_user_id,
            )
            return RESTfulResponse(appintments).to_serializable()

        appintments, appintment_total_counts = appintment_service.get_all(
            page=page,
            per_page=per_page,
            line_user_id=line_user_id, 
            payload=jwt_payload, 
            with_total_count=True
        )
        return RESTfulResponse(appintments, pagination=(page, per_page, appintment_total_counts)).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<line_user_id>", methods=["GET"])
@verify_access_token(access_roles=["line_bot"])
def get_line_member_endpoint(line_user_id):
    try:
        user_data = user_service.get_one(line_user_id=line_user_id)
        return RESTfulResponse(user_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("", methods=["GET"])
@verify_access_token(access_roles=["admin"])
def get_all_endpoint():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        query = request.args.get("query", None, type=str)
        status = request.args.get("status", None, type=int)
        user_dataset, total_items_count = user_service.get_all(
            page=page,
            per_page=per_page,
            query=query,
            status=status,
            with_total_items=True,
        )
        return RESTfulResponse(
            user_dataset,
            hide_fields=["is_deleted"],
            pagination=(page, per_page, total_items_count),
        ).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:user_id>", methods=["PUT"])
@verify_access_token(check_owner=True)
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
                "line_user_id": str,
                "is_active": bool,
                "is_deleted": bool,
                "role": str,
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
        request_validator.check(request)
        user_json_data = request.get_json()
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        updated_user_data = user_service.update_one(user_id, user_json_data, payload=jwt_payload)
        return RESTfulResponse(
            updated_user_data
        ).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:user_id>", methods=["DELETE"])
@verify_access_token(check_owner=True)
def delete_endpoint(user_id):
    try:
        deleted_user_data = user_service.delete_one(user_id)
        return RESTfulResponse(
            deleted_user_data
        ).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)
