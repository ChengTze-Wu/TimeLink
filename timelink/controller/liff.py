from flask import Blueprint, render_template

liff = Blueprint('liff', __name__)

@liff.route("/services", methods=['GET'])
def liff_services():
    return render_template('liff/services.html')

@liff.route("/service/<service_id>", methods=['GET'])
def liff_service(service_id):
    return render_template("liff/service.html")