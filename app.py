# import logging

import os

from dotenv import load_dotenv
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from authentication_app.models import bcrypt, db
from authentication_app.models.user import User
from authentication_app.urls.admin import authentication_app_admin
from authentication_app.urls.authenticated import authentication_app_authenticated
from authentication_app.urls.public import authentication_app_public


def create_app():
    load_dotenv()
    # start_logging()

    # logging.info("Loading environment variables (from .env)")

    # logging.info("Creating the flask app")
    app = Flask(__name__)

    # logging.info("Loading variables from config.py")
    app.config.from_object("config")
    app.config["UPLOADED_IMAGES_DEST"] = "static/uploads/images"

    # logging.info("Registering authentication_app (a Blueprint)")
    app.register_blueprint(authentication_app_public)
    app.register_blueprint(authentication_app_admin)
    app.register_blueprint(authentication_app_authenticated)

    # Bootstrap-Flask requires this line
    bootstrap = Bootstrap5()
    bootstrap.init_app(app)

    # Flask-WTF requires this line
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Flask-Bcrypt requires this line
    bcrypt.init_app(app)

    # flask_login requires this line
    login_manager = LoginManager()
    # flask_login requires this line
    login_manager.init_app(app)
    # redirect to login view if user is not connected
    login_manager.login_view = "authentication_app.login"

    # flask_login requires this function
    @login_manager.user_loader
    def load_user(user_id):
        """load current_user data from database when the user connects"""

        return User.query.get(int(user_id))

    # flask_sqlalchemy requires this line
    # Initialize SQLAlchemy() with app
    db.init_app(app)

    # flask_migrate requires this line
    # allow to make migrations with CLI :
    # 1. flask db init : to initialize the migration folder
    # 2. flask db migrate -m 'migration name' : make migrations
    # 3. flask db upgrade : migrate
    migrate = Migrate()
    migrate.init_app(app, db)

    with app.app_context():
        if not os.path.exists("app.db"):
            db.create_all()
            User.create_admin()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
