from flask import Blueprint, request, abort
from web_api.validators.request_vaildator import RequestValidator
from web_api.views.response_view import RESTfulResponse
from web_api.services import group_service
from werkzeug.exceptions import HTTPException

bp = Blueprint("group_router", __name__)


@bp.route("", methods=["POST"])
def create_endpoint():
    try:
        request_validator = RequestValidator(
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
            }
        )
        request_validator.check(request)
        
        group_json_data = request.get_json()
        created_group_data = group_service.create_one(group_json_data)
        return RESTfulResponse(created_group_data).to_serializable(), 201
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:group_id>", methods=["PUT"])
def update_endpoint(group_id):
    try:
        request_validator = RequestValidator(
            request_type="json",
            field_types={
                "name": str,
                "line_group_id": str,
                "is_active": bool,
            },
            field_max_lengths={
                "name": 100,
                "line_group_id": 100,
            }
        )
        request_validator.check(request)

        group_json_data = request.get_json()
        updated_group_data = group_service.update_one_by_id(group_json_data, group_id)
        return RESTfulResponse(updated_group_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:group_id>", methods=["DELETE"])
def delete_endpoint(group_id):
    try:
        deleted_group_data = group_service.logical_delete_by_id(group_id)
        return RESTfulResponse(deleted_group_data).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)


@bp.route("/<uuid:group_id>", methods=["GET"])
def get_one_endpoint(group_id):
    try:
        group_data = group_service.get_one_by_id(group_id)
        return RESTfulResponse(group_data).to_serializable()
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
        group_dataset, total_items_count = group_service.get_all_available_by_filter(
            page=page,
            per_page=per_page,
            query=query,
            status=status,
            with_total_items=True,
        )
        return RESTfulResponse(group_dataset, pagination=(page, per_page, total_items_count)).to_serializable()
    except HTTPException as e:
        abort(e.code, e.description)
    except Exception as e:
        abort(500, e)