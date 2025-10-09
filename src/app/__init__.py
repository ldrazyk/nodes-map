from flask import Flask
from .model import Application

def create_app():

    app = Flask(__name__)

    global application
    application = Application()

    from .main.routes import main
    app.register_blueprint(main)
    from .api.routes import api
    app.register_blueprint(api, url_prefix="/api")

    return app