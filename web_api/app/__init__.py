from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask

def create_app(test_config=None):

    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        __name__,
        root_path=ROOT_PATH
    )

    app.json.sort_keys = False  # [2023-11-06 Tze] To make the JSON response ordered

    if test_config is not None:
        app.config.from_mapping(test_config)

    with app.app_context():
        from .routers import user_router, auth_router, service_router, group_router, appointment_router
        from .utils import error_handlers
        from .tools.cli import create_jwt

        app.cli.add_command(create_jwt)

        app.register_error_handler(400, error_handlers.handle_400_error)
        app.register_error_handler(401, error_handlers.handle_401_error)
        app.register_error_handler(403, error_handlers.handle_403_error)
        app.register_error_handler(404, error_handlers.handle_404_error)
        app.register_error_handler(405, error_handlers.handle_405_error)
        app.register_error_handler(409, error_handlers.handle_409_error)
        app.register_error_handler(500, error_handlers.handle_500_error)

        app.register_blueprint(user_router.bp, url_prefix='/api/users')
        app.register_blueprint(service_router.bp, url_prefix='/api/services')
        app.register_blueprint(group_router.bp, url_prefix='/api/groups')
        app.register_blueprint(appointment_router.bp, url_prefix='/api/appointments')
        app.register_blueprint(auth_router.bp, url_prefix='/api/auth')
    return app
