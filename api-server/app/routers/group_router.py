from flask import Blueprint, request, abort
from app.utils.validators.request_vaildator import RequestValidator
from app.views.response_view import RESTfulResponse
from app.services import GroupService, ServiceService, UserService
from werkzeug.exceptions import HTTPException
from requests.exceptions import RequestException
from app.utils.validators.token_validator import verify_access_token
from app.utils.handlers.jwt_handler import JWTHandler


bp = Blueprint("group_router", __name__)
group_service = GroupService()
service_service = ServiceService()
user_service = UserService()
jwt_handler = JWTHandler()


@bp.route("", methods=["POST"])
@verify_access_token(access_roles=["group_owner"])
def link_bot_endpoint():
    try:
        request_validator = RequestValidator(
            request_type="json",
            required_fields=["line_group_id"],
            field_types={
                "line_group_id": str,
                "is_active": bool,
            },
        )
        request_validator.check(request)
        group_json_data = request.get_json()
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        created_group_data = group_service.create_one(group_json_data, payload=jwt_payload)
        return RESTfulResponse(created_group_data).to_serializable(), 201
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)


@bp.route("/<line_group_id>/users/<line_user_id>", methods=["POST"])
@verify_access_token(access_roles=["line_bot"])
def link_user_endpoint(line_group_id, line_user_id):
    try:
        created_group_data = group_service.link_user_to_group(
            line_group_id=line_group_id, line_user_id=line_user_id
        )
        return RESTfulResponse(created_group_data).to_serializable(), 201
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)


@bp.route("/<line_group_id>/users/<line_user_id>", methods=["DELETE"])
@verify_access_token(access_roles=["line_bot"])
def unlink_user_endpoint(line_group_id, line_user_id):
    try:
        deleted_group_data = group_service.unlink_user_from_group(
            line_group_id=line_group_id, line_user_id=line_user_id
        )
        return RESTfulResponse(deleted_group_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except RequestException as e:
        abort(e.response.status_code, e.response.text)
    except Exception as e:
        abort(500, e)


@bp.route("", methods=["GET"])
@verify_access_token(access_roles=["admin", "group_owner"])
def get_all_endpoint():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        query = request.args.get("query", None, type=str)
        status = request.args.get("status", None, type=int)
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        group_dataset, total_items_count = group_service.get_all(
            page=page,
            per_page=per_page,
            query=query,
            status=status,
            with_total_items=True,
            payload=jwt_payload,
        )
        return RESTfulResponse(
            group_dataset, pagination=(page, per_page, total_items_count)
        ).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:group_id>", methods=["GET"])
@verify_access_token(access_roles=["admin", "group_owner"])
def get_one_endpoint(group_id):
    try:
        print(type(group_id))
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        group_data = group_service.get_one(group_id=group_id, payload=jwt_payload)
        return RESTfulResponse(group_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/line/<line_group_id>", methods=["GET"])
@verify_access_token(access_roles=["line_bot", "liff"])
def get_line_group_endpoint(line_group_id):
    try:
        group_data = group_service.get_one(line_group_id=line_group_id)
        return RESTfulResponse(group_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<line_group_id>/services", methods=["GET"])
@verify_access_token(access_roles=["line_bot", "liff"])
def get_group_services_endpoint(line_group_id):
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        popular = request.args.get("popular", None, type=int)

        if popular:
            service_dataset = service_service.get_most_popular_by_line_group_id(
                line_group_id=line_group_id, limit=popular
            )
            return RESTfulResponse(service_dataset).to_serializable()

        service_dataset, total_items_count = service_service.get_all(
            line_group_id=line_group_id, with_total_items=True
        )
        return RESTfulResponse(service_dataset, pagination=(page, per_page, total_items_count)).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:group_id>/users", methods=["GET"])
@verify_access_token(access_roles=["admin", "group_owner"])
def get_group_users_endpoint(group_id):
    try:
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        service_dataset, total_items_count = user_service.get_all(
            group_id=group_id, with_total_items=True, page=page, per_page=per_page, payload=jwt_payload
        )
        return RESTfulResponse(service_dataset, pagination=(page, per_page, total_items_count)).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:group_id>", methods=["PUT"])
@verify_access_token(access_roles=["admin", "group_owner"])
def update_endpoint(group_id):
    try:
        request_validator = RequestValidator(
            request_type="json",
            field_types={
                "is_active": bool,
            },
        )
        request_validator.check(request)
        group_json_data = request.get_json()
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        updated_group_data = group_service.update_one(group_id, group_json_data, payload=jwt_payload)
        return RESTfulResponse(updated_group_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:group_id>", methods=["DELETE"])
@verify_access_token(access_roles=["admin", "group_owner"])
def delete_endpoint(group_id):
    try:
        jwt_payload = jwt_handler.get_payload(request.headers.get("Authorization"))
        deleted_group_data = group_service.delete_one(group_id, payload=jwt_payload)
        return RESTfulResponse(deleted_group_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)
