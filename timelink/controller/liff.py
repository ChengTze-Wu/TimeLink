from flask import Blueprint, render_template

bp = Blueprint('liff', __name__, url_prefix='/liff')

@bp.route("/services", methods=['GET'])
def liff_services():
    return render_template('liff/services.html')

@bp.route("/service/<service_id>", methods=['GET'])
def liff_service(service_id):
    return render_template("liff/service.html")