from dotenv import load_dotenv
from flask import Flask

from config import Config
from .db import init_database


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)

    # Register routes first
    from .routes import main
    app.register_blueprint(main)

    # Initialize database (won't crash the app if it fails)
    with app.app_context():
        try:
            init_database()
        except Exception as e:
            print(f"Database initialization warning: {e}")

    return app