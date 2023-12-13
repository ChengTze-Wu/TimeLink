from flask import Blueprint, request, abort
from web_api.utils.validators import RequestValidator
from web_api.views.response_view import RESTfulResponse
from web_api.services import service_service


bp = Blueprint("service_router", __name__)


@bp.route("", methods=["POST"])
def create():
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
            "unavailable_datetime": str,
            "is_active": bool,
        },
        field_max_lengths={
            "name": 100,
            "image": 100,
            "start_date": 100,
            "end_date": 100,
            "unavailable_datetime": 100,
        },
    )
    is_valid = request_validator.check()
    if not is_valid:
        abort(400, request_validator.message)

    service_json_data = request.get_json()
    service = service_service.create_one(service_json_data)
    return RESTfulResponse(service).to_dict(), 201




@bp.route("/<service_id>", methods=["DELETE"])
def delete(service_id):
    service = service_service.logical_delete(service_id)
    return RESTfulResponse(service).to_dict()


@bp.route("/<service_id>", methods=["PUT"])
def update(service_id):
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
            "unavailable_datetime": str,
            "is_active": bool,
        },
        field_max_lengths={
            "name": 100,
            "image": 100,
            "start_date": 100,
            "end_date": 100,
            "unavailable_datetime": 100,
        },
    )
    is_valid = request_validator.check()
    if not is_valid:
        abort(400, request_validator.message)

    service_json_data = request.get_json()
    service = service_service.update_one(service_id, service_json_data)
    return RESTfulResponse(service).to_dict()


@bp.route("/<service_id>", methods=["GET"])
def get_one(service_id):
    service = service_service.get_one(service_id)
    return RESTfulResponse(service).to_dict()



@bp.route("", methods=["GET"])
def get_all():
    services = service_service.get_all()
    return RESTfulResponse(services).to_dict()


@bp.route("/<service_id>/groups", methods=["GET"])
def get_groups(service_id):
    groups = service_service.get_groups(service_id)
    return RESTfulResponse(groups).to_dict()


@bp.route("/<service_id>/users", methods=["GET"])
def get_users(service_id):
    users = service_service.get_users(service_id)
    return RESTfulResponse(users).to_dict()


