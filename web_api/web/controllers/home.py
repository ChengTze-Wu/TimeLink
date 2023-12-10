from flask import Blueprint, render_template

bp = Blueprint('home', __name__)

@bp.route("/", methods=['GET'])
def index():
    return render_template('home/home.html')

@bp.route("/signup", methods=['GET'])
def signup():
    return render_template('home/signup.html')