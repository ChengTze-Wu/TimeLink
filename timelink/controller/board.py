from flask import Blueprint, render_template
from timelink.util.login_validator import login_required

bp = Blueprint('board', __name__, url_prefix='/board')

@bp.route("/", methods=['GET'])
@login_required
def index():
    return render_template('board/board.html')

@bp.route("/service", methods=['GET'])
@login_required
def service():
    return render_template('board/service.html')

@bp.route("/reserve", methods=['GET'])
@login_required
def reserve():
    return render_template('board/reserve.html')

@bp.route("/group", methods=['GET'])
@login_required
def group():
    return render_template('board/group.html')

@bp.route("/member", methods=['GET'])
@login_required
def member():
    return render_template('board/member.html')