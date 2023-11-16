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
from club_app.models.club import Club
from club_app.urls.admin import club_app_admin
from club_app.urls.authenticated import club_app_authenticated
from club_app.urls.public import club_app_public
from competition_app.models.competition import Competition
from competition_app.urls.admin import competition_app_admin
from competition_app.urls.authenticated import competition_app_authenticated
from competition_app.urls.public import competition_app_public


def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)

    app.config.from_object("config")

    app.register_blueprint(authentication_app_public)
    app.register_blueprint(authentication_app_authenticated)
    app.register_blueprint(authentication_app_admin)

    app.register_blueprint(club_app_public)
    app.register_blueprint(club_app_authenticated)
    app.register_blueprint(club_app_admin)

    app.register_blueprint(competition_app_public)
    app.register_blueprint(competition_app_authenticated)
    app.register_blueprint(competition_app_admin)

    # Bootstrap-Flask requires these lines
    bootstrap = Bootstrap5()
    bootstrap.init_app(app)

    # Flask-WTF requires these lines
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Flask-Bcrypt requires these lines
    bcrypt.init_app(app)

    # flask_login requires these lines
    login_manager = LoginManager()
    login_manager.init_app(app)
    # redirect to login view if current_user is not connected
    login_manager.login_view = "authentication_app_public.login"

    @login_manager.user_loader
    def load_user(user_id):
        """load current_user data from database when the user connects"""

        return User.query.get(int(user_id))

    # flask_sqlalchemy requires this line
    db.init_app(app)

    # flask_migrate requires these lines
    # allow to make migrations with CLI :
    # 1. flask db init : to initialize the migration folder
    # 2. flask db migrate -m 'migration name' : make migrations
    # 3. flask db upgrade : migrate
    migrate = Migrate()
    migrate.init_app(app, db)

    with app.app_context():
        if not os.path.exists("app.db"):
            User.init_db()
            Club.init_db()
            Competition.init_db()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
