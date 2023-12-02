from flask import Blueprint, request
from web_app.api.services import account_service

bp = Blueprint("auth", __name__)


@bp.route("/", methods=["GET"])
def login():
    pass


@bp.route("/", methods=["DELETE"])
def logout():
    pass
