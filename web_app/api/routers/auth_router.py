from flask import Blueprint, request
from web_app.api.services import account_service
from web_app.utils.validators import RequestValidator, PasswordValidator
from web_app.api.views.response_view import RESTfulResponse


bp = Blueprint("auth_router", __name__)


@bp.route("/", methods=["GET"])
def login():
    pass


@bp.route("/", methods=["DELETE"])
def logout():
    pass
