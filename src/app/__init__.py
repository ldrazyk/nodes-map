from flask import Flask
from .model import Application, EmbeddingsProcessor

def create_app():

    app = Flask(__name__)

    global embeddings_processor
    embeddings_processor = EmbeddingsProcessor(random_state=33)
    global application
    application = Application()

    from .main.routes import main
    app.register_blueprint(main)
    from .api.routes import api
    app.register_blueprint(api, url_prefix="/api")

    return app