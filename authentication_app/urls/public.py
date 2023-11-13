from flask import Blueprint

from authentication_app.views.public import (
    ForgottenPassword,
    Home,
    Login,
    Logout,
    Signup,
    ResetPassword
)

authentication_app_public = Blueprint(
    "authentication_app_public",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)
authentication_app_public.add_url_rule("/signup/", view_func=Signup.as_view("signup"))
authentication_app_public.add_url_rule("/login/", view_func=Login.as_view("login"))
authentication_app_public.add_url_rule("/logout/", view_func=Logout.as_view("logout"))
authentication_app_public.add_url_rule("/", view_func=Home.as_view("home"))
authentication_app_public.add_url_rule(
    "/forgotten-password/",
    view_func=ForgottenPassword.as_view("forgotten_password"),
)
authentication_app_public.add_url_rule(
    "/reset-password/<token>/",
    view_func=ResetPassword.as_view("reset_password"),
)
