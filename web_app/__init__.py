import os
from flask import Flask

# from flask_socketio import SocketIO

# socketio = SocketIO(cors_allowed_origins=["https://timelink.cc",
#                                           "https://www.timelink.cc",
#                                           "http://127.0.0.1:8000"])

def create_app(test_config=None):

    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        __name__,
        root_path=ROOT_PATH,
        instance_relative_config=True,
        instance_path=os.path.join(
            ROOT_PATH, "configs"
        ),
    )

    app.config.from_mapping(
        SECRET_KEY='test',
    )

    app.json.sort_keys = False  # [2023-11-06 Tze] To make the JSON response ordered

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from web_app.api import routers
        from web_app.utils import error_handlers

        app.register_error_handler(400, error_handlers.handle_400_error)
        app.register_error_handler(401, error_handlers.handle_401_error)
        app.register_error_handler(403, error_handlers.handle_403_error)
        app.register_error_handler(404, error_handlers.handle_404_error)
        app.register_error_handler(405, error_handlers.handle_405_error)
        app.register_error_handler(409, error_handlers.handle_409_error)
        app.register_error_handler(500, error_handlers.handle_500_error)

        app.register_blueprint(routers.user_router.bp, url_prefix='/api/users')
        app.register_blueprint(routers.auth_router.bp, url_prefix='/api/auth')
    return app
