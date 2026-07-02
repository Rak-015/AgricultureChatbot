import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "agri-bot-local-secret-key")
    UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads"
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Mysql@123")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "agribot")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MODEL_PATH = Path(os.getenv("MODEL_PATH", BASE_DIR / "app" / "ml" / "mobilenet.h5"))
    FALLBACK_MODEL_PATH = os.getenv("FALLBACK_MODEL_PATH") or None
