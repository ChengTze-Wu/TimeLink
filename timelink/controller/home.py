from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route("/", methods=['GET'])
def index():
    return render_template('home/home.html')

@home.route("/signup", methods=['GET'])
def signup():
    return render_template('home/signup.html')