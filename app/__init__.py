from dotenv import load_dotenv
from flask import Flask

from config import Config


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)
    from .routes import main
    app.register_blueprint(main)
    return app
