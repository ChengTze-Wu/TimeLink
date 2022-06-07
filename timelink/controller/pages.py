from flask import Blueprint, render_template
from util import login_required


pages = Blueprint('pages', __name__)


@pages.route("/")
@login_required
def index():
    return render_template('index.html')

@pages.route("/service")
@login_required
def service():
    return render_template('service.html')

@pages.route("/reserve")
@login_required
def reserve():
    return render_template('reserve.html')

@pages.route("/group")
@login_required
def group():
    return render_template('group.html')

@pages.route("/member")
@login_required
def member():
    return render_template('member.html')

@pages.route("/signin")
def signin():
    return render_template('signin.html')

@pages.route("/signup")
def signup():
    return render_template('signup.html')