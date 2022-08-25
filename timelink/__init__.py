from flask import Flask

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_pyfile('timelink_config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        
    from timelink.model import db
    db.init_app(app)
    
    with app.app_context():
    # pages
        from . import controller
        app.register_blueprint(controller.home.bp)
        app.register_blueprint(controller.board.bp)
        app.register_blueprint(controller.liff.bp)
        # apis
        app.register_blueprint(controller.apis.group.bp)
        app.register_blueprint(controller.apis.member.bp)
        app.register_blueprint(controller.apis.reserve.bp)
        app.register_blueprint(controller.apis.service.bp)
        app.register_blueprint(controller.apis.user.bp)
    
    return app