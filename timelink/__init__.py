from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO

csrf = CSRFProtect()
socketio = SocketIO(cors_allowed_origins='*')

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_pyfile('timelink_config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        
    from timelink.model import db
    csrf.init_app(app)
    db.init_app(app)
    socketio.init_app(app)
    
    with app.app_context():
        from . import controller
        # pages
        app.register_blueprint(controller.home.bp)
        app.register_blueprint(controller.board.bp)
        app.register_blueprint(controller.liff.bp)
        # apis
        app.register_blueprint(controller.apis.group.bp)
        # app.register_blueprint(controller.apis.member.bp)
        app.register_blueprint(controller.apis.reserve.bp)
        app.register_blueprint(controller.apis.service.bp)
        app.register_blueprint(controller.apis.user.bp)
    
    return app