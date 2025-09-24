from flask import Flask
from .model import utils

def create_app():

    app = Flask(__name__)

    global utils

    from .main.routes import main
    app.register_blueprint(main)
    from .api.routes import api
    app.register_blueprint(api, url_prefix="/api")

    return app