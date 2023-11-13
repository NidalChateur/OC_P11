from datetime import datetime

from flask import flash, redirect, render_template, url_for
from flask.views import MethodView
from flask_login import current_user, login_user, logout_user

from authentication_app.forms.public import (
    ForgottenPasswordForm,
    LoginForm,
    ResetPasswordForm,
    SignupForm,
)
from authentication_app.models.user import User
from email_app.send_email import send_email
from email_app.templates import (
    RESET_PASSWORD_CONTENT,
    RESET_PASSWORD_SUBJECT,
    SIGNUP_CONTENT,
    SIGNUP_SUBJECT,
)


class Signup(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for("authentication_app_public.home"))
        form = SignupForm()

        return render_template("user_form.html", form=form)

    def post(self):
        form = SignupForm()
        if form.validate_on_submit():
            user = User(
                role="secretary",
                first_name=form.first_name.data.capitalize(),
                last_name=form.last_name.data.capitalize(),
                birthdate=form.birthdate.data,
                email=form.email.data.lower(),
            )
            user.is_activated = False
            user.create()

            user.set_password(form.password.data)

            if form.image.data:
                user.resize_and_save_image(form.image.data)

            send_email(
                to=user.email,
                subject=SIGNUP_SUBJECT,
                content=SIGNUP_CONTENT.format(user.first_name),
            )

            flash("Demande de création de compte envoyée !", "success")

            return redirect(url_for("authentication_app_public.login"))

        return render_template("user_form.html", form=form)


class Login(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for("authentication_app_public.home"))
        form = LoginForm()

        return render_template("user_form.html", form=form)

    def post(self):
        form = LoginForm()
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            login_user(user)

            flash("Connexion réussie !", "success")

            return redirect(url_for("authentication_app_public.home"))

        return render_template("user_form.html", form=form)


class Logout(MethodView):
    def get(self):
        logout_user()
        flash("Vous êtes déconnecté.", "info")

        return redirect(url_for("authentication_app_public.login"))


class Home(MethodView):
    def get(self):
        return render_template("home.html")


class ForgottenPassword(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for("authentication_app_public.home"))

        form = ForgottenPasswordForm()

        return render_template("user_form.html", form=form)

    def post(self):
        form = ForgottenPasswordForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.lower()).first()

            user.generate_reset_token()
            url = url_for(
                "authentication_app_public.reset_password",
                token=user.token,
                _external=True,
            )

            send_email(
                to=user.email,
                subject=RESET_PASSWORD_SUBJECT,
                content=RESET_PASSWORD_CONTENT.format(user.first_name, url),
            )

            flash(
                "Un email de réinitialisation de mot de passe a été envoyé à votre adresse email.",
                "info",
            )

            return redirect(url_for("authentication_app_public.login"))

        return render_template("user_form.html", form=form)


class ResetPassword(MethodView):
    def get(self, token):
        if current_user.is_authenticated:
            return redirect(url_for("authentication_app_public.home"))
        form = ResetPasswordForm()

        return render_template("user_form.html", form=form)

    def post(self, token):
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user = User.query.filter_by(token=token).first()
            if user and user.token_expiration_date > datetime.utcnow():
                user.set_password(form.password.data)
                flash("Votre mot de passe a été réinitialisé avec succès.", "success")
            else:
                flash(
                    "La demande de réinitialisation de mot de passe est invalide ou a expiré.",
                    "error",
                )

            return redirect(url_for("authentication_app_public.login"))

        return render_template("user_form.html", form=form)
