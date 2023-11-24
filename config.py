from pathlib import Path


class Config:
    SECRET_KEY = "316242afe7c0e1588fffec66ff9108120771d727b59e4e60"
    BASE_DIR = Path(__file__).resolve().parent
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "static"
    DEBUG = True


class Development(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(Config.BASE_DIR / "app.db")
    WTF_CSRF_ENABLED = False


class Testing(Config):
    DATABASE = Config.BASE_DIR / "tests/app_test.db"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(Config.BASE_DIR / "tests/app_test.db")
    LIVESERVER_PORT = 8943
    LIVESERVER_TIMEOUT = 10
    SERVER_NAME = "localhost:8943"
    WTF_CSRF_ENABLED = False


class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://utilisateur:mdp@localhost/production"
