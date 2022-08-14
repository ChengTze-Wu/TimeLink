from flask import Blueprint, render_template
from timelink.util.login_validator import login_required

bp = Blueprint('board', __name__)

@bp.route("/board", methods=['GET'])
@login_required
def index():
    return render_template('board/board.html')

@bp.route("/board/service", methods=['GET'])
@login_required
def service():
    return render_template('board/service.html')

@bp.route("/board/reserve", methods=['GET'])
@login_required
def reserve():
    return render_template('board/reserve.html')

@bp.route("/board/group", methods=['GET'])
@login_required
def group():
    return render_template('board/group.html')

@bp.route("/board/member", methods=['GET'])
@login_required
def member():
    return render_template('board/member.html')