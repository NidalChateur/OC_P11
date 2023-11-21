from flask import url_for

from authentication_app.models.user import User, db
from authentication_app.views.public import (
    ForgottenPassword,
    Login,
    Logout,
    ResetPassword,
    Signup,
)


class Test_User_Urls_Public:
    def test_signup_url(self, app):
        # 1. path check
        endpoint = url_for("authentication_app_public.signup")
        assert endpoint == "/signup/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match("/signup/")
        assert view_name == "authentication_app_public.signup"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == Signup

    def test_login_url(self, app):
        # 1. path check
        endpoint = url_for("authentication_app_public.login")
        assert endpoint == "/login/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match("/login/")
        assert view_name == "authentication_app_public.login"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == Login

    def test_logout_url(self, app):
        # 1. path check
        endpoint = url_for("authentication_app_public.logout")
        assert endpoint == "/logout/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match("/logout/")
        assert view_name == "authentication_app_public.logout"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == Logout

    def test_forgotten_password_url(self, app):
        # 1. path check
        endpoint = url_for("authentication_app_public.forgotten_password")
        assert endpoint == "/forgotten-password/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match("/forgotten-password/")
        assert view_name == "authentication_app_public.forgotten_password"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == ForgottenPassword

    def test_reset_password_url(self, app):
        # 0. generate a token
        user_1 = db.session.get(User, 1)
        user_1.generate_reset_token()
        token = user_1.token

        # 1. path check
        endpoint = url_for("authentication_app_public.reset_password", token=token)
        assert endpoint == "/reset-password/" + token + "/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match(
            "/reset-password/" + token + "/"
        )
        assert view_name == "authentication_app_public.reset_password"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == ResetPassword
