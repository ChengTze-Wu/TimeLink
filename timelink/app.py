import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()
import controller


app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

# apis
app.register_blueprint(controller.apis.service, url_prefix="/api")
app.register_blueprint(controller.apis.group, url_prefix="/api")
app.register_blueprint(controller.apis.user, url_prefix="/api")
app.register_blueprint(controller.apis.reserve, url_prefix="/api")
# apps
app.register_blueprint(controller.home)
app.register_blueprint(controller.board, url_prefix="/board")
app.register_blueprint(controller.liff, url_prefix="/liff")