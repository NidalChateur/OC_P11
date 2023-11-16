from flask import flash, redirect, render_template, url_for
from flask.views import MethodView
from flask_login import current_user, login_required, logout_user

from authentication_app.forms.authenticated import (
    AddMyPhotoForm,
    ChangeMyPasswordForm,
    UpdateMyProfileForm,
)
from authentication_app.models.user import User
from club_app.models.club import Club


class MyProfile(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("my_profile.html")


class UpdateMyProfile(MethodView):
    decorators = [login_required]

    def get(self):
        user = User.query.get(current_user.id)
        form = UpdateMyProfileForm(obj=user)

        return render_template("user_form.html", form=form)

    def post(self):
        user = User.query.get(current_user.id)
        form = UpdateMyProfileForm(obj=user)

        if user and form.validate_on_submit():
            used_email = User.query.filter_by(email=form.email.data.lower()).first()
            if user.email != form.email.data.lower() and used_email:
                form.email.errors.append(
                    "Cet e-mail est déjà utilisé par un utilisateur !"
                )
            else:
                user.first_name = form.first_name.data.capitalize()
                user.last_name = form.last_name.data.capitalize()
                user.birthdate = form.birthdate.data
                user.email = form.email.data.lower()
                user.save()
                flash(
                    "Votre compte utilisateur a été mis à jour avec succès !", "success"
                )

                return redirect(url_for("authentication_app_authenticated.my_profile"))

        return render_template("user_form.html", form=form)


class AddMyPhoto(MethodView):
    decorators = [login_required]

    def get(self):
        form = AddMyPhotoForm()

        return render_template("user_form.html", form=form)

    def post(self):
        user = User.query.get(current_user.id)
        form = AddMyPhotoForm()
        if form.validate_on_submit():
            if form.image.data:
                user.resize_and_save_image(form.image.data)
                flash("Votre photo de profil a été mis à jour avec succès !", "success")

            return redirect(url_for("authentication_app_authenticated.my_profile"))

        return render_template("user_form.html", form=form)


class DeleteMyPhoto(MethodView):
    decorators = [login_required]

    def get(self):
        user = User.query.get(current_user.id)
        if user.image:
            user.delete_image()
            flash("Votre photo de profil a été mis à jour avec succès !", "success")
        else:
            flash("Vous n'avez pas de photo de profil à supprimer !", "info")

        return redirect(url_for("authentication_app_authenticated.my_profile"))


class DeleteMyAccountConfirmation(MethodView):
    decorators = [login_required]

    def get(self):
        user = User.query.get(current_user.id)

        return render_template(
            "delete_user_confirmation.html", user=user, delete_from_my_profile=True
        )


class DeleteMyAccount(MethodView):
    decorators = [login_required]

    def get(self):
        user = User.query.get(current_user.id)
        club = Club.query.filter_by(secretary_id=user.id).first()
        if club:
            club.secretary_id = None
            club.save()

        user.delete()
        logout_user()

        flash("Votre compte utilisateur a été supprimé.", "info")

        return redirect(url_for("authentication_app_public.login"))


class ChangeMyPassword(MethodView):
    decorators = [login_required]

    def get(self):
        form = ChangeMyPasswordForm()

        return render_template("user_form.html", form=form)

    def post(self):
        user = User.query.get(current_user.id)
        form = ChangeMyPasswordForm()
        if form.validate_on_submit():
            if not user.is_a_valid_password(form.old_password.data):
                form.old_password.errors.append("Mot de passe incorrect !")
            else:
                user.set_password(form.password.data)
                flash("Votre mot de passe a été modifié avec succès !", "success")

                return redirect(url_for("authentication_app_authenticated.my_profile"))

        return render_template("user_form.html", form=form)
