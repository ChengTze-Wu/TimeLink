from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
from datetime import datetime


def handle_400_error(e: HTTPException):
    current_app.logger.error(e)
    return (
        jsonify(
            {
                "message": e.description
                if isinstance(e.description, list)
                else [e.description],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ),
        400,
    )


def handle_401_error(e: HTTPException):
    current_app.logger.error(e)
    return (
        jsonify(
            {
                "message": e.description
                if isinstance(e.description, list)
                else [e.description],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ),
        401,
    )


def handle_403_error(e: HTTPException):
    current_app.logger.error(e)
    return (
        jsonify(
            {
                "message": e.description
                if isinstance(e.description, list)
                else [e.description],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ),
        403,
    )


def handle_404_error(e: HTTPException):
    current_app.logger.error(e)
    return (
        jsonify(
            {
                "message": e.description
                if isinstance(e.description, list)
                else [e.description],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ),
        404,
    )


def handle_405_error(e):
    current_app.logger.error(e)
    return (
        jsonify(
            {
                "message": ["Method not allowed"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ),
        405,
    )


def handle_409_error(e: HTTPException):
    current_app.logger.error(e)
    return (
        jsonify(
            {
                "message": e.description
                if isinstance(e.description, list)
                else [e.description],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ),
        409,
    )


def handle_500_error(e: Exception):
    current_app.logger.error(e, exc_info=True)
    return (
        jsonify(
            {
                "message": ["Internal server error"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ),
        500,
    )
