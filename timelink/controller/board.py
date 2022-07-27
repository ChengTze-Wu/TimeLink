from flask import Blueprint, render_template
from util import login_required


board = Blueprint('board', __name__)


@board.route("/", methods=['GET'])
@login_required
def index():
    return render_template('board/board.html')

@board.route("/service", methods=['GET'])
@login_required
def service():
    return render_template('board/service.html')

@board.route("/reserve", methods=['GET'])
@login_required
def reserve():
    return render_template('board/reserve.html')

@board.route("/group", methods=['GET'])
@login_required
def group():
    return render_template('board/group.html')

@board.route("/member", methods=['GET'])
@login_required
def member():
    return render_template('board/member.html')