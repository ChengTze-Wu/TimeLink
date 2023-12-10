from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException

def handle_400_error(e: HTTPException):
    current_app.logger.error(e)
    return jsonify({"message": e.description}), 400

def handle_401_error(e: HTTPException):
    current_app.logger.error(e)
    return jsonify({"message": e.description}), 401

def handle_403_error(e: HTTPException):
    current_app.logger.error(e)
    return jsonify({"message": e.description}), 403

def handle_404_error(e: HTTPException):
    current_app.logger.error(e)
    return jsonify({"message": e.description}), 404

def handle_405_error(e):
    current_app.logger.error(e)
    return jsonify({"message": "Method not allowed"}), 405

def handle_409_error(e: HTTPException):
    current_app.logger.error(e)
    return jsonify({"message": e.description}), 409

def handle_500_error(e: HTTPException):
    current_app.logger.error(e, exc_info=True)
    return jsonify({"message": "Server error"}), 500