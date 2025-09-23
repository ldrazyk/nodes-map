from flask import Flask
from .model import Model

def create_app():

    app = Flask(__name__)

    global app_model
    app_model = Model()

    from .main.routes import main
    app.register_blueprint(main)

    return app