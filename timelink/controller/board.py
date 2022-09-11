from flask import Blueprint, render_template
from timelink.util.login_validator import login_required

bp = Blueprint('board', __name__)

@bp.route("/board/guide", methods=['GET'])
@login_required
def guide():
    return render_template('board/guide.html')

@bp.route("/board/service", methods=['GET'])
@login_required
def service():
    return render_template('board/service.html')

@bp.route("/board/reserve", methods=['GET'])
@bp.route("/board/reserve/<int:reserve_id>", methods=['GET'])
@login_required
def reserve(reserve_id=None):
    if reserve_id:
        return render_template('board/reserve.html', reserve_id=reserve_id)
    return render_template('board/reserves.html')

@bp.route("/board/group", methods=['GET'])
@login_required
def group():
    return render_template('board/group.html')

@bp.route("/board/member", methods=['GET'])
@login_required
def member():
    return render_template('board/member.html')