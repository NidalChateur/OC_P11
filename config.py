import logging
from pathlib import Path

SECRET_KEY = "316242afe7c0e1588fffec66ff9108120771d727b59e4e60"

BASE_DIR = Path(__file__).resolve().parent

SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = "static"


# créer un package logging
LOG_FILE_PATH = BASE_DIR / "logging/myapp.log"


def print_info():
    print("The logging is recorded in ./logging/myapp.log")
    print("* Running on http://127.0.0.1:5000")


def start_logging():
    """create ./logging/myapp.log file and write logs"""

    print_info()
    with open(LOG_FILE_PATH, "w"):
        pass
    # Write the logs to logging/myapp.log
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename=LOG_FILE_PATH,
    )
