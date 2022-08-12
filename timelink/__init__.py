from flask import Flask

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_pyfile('timelink_config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        
    from timelink.model import db
    db.init_app(app)
    
    # pages
    from timelink.controller import home, board, liff
    app.register_blueprint(home.bp)
    app.register_blueprint(board.bp)
    app.register_blueprint(liff.bp)
    
    # apis

    return app