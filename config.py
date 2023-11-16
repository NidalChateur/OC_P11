from pathlib import Path

SECRET_KEY = "316242afe7c0e1588fffec66ff9108120771d727b59e4e60"

BASE_DIR = Path(__file__).resolve().parent

SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = "static"
