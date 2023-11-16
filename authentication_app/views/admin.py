from flask import flash, redirect, render_template, url_for
from flask.views import MethodView
from flask_login import current_user, logout_user

from authentication_app.decorator import admin_required
from authentication_app.forms.admin import CreateUserForm, UpdateUserForm
from authentication_app.models.user import User
from club_app.models.club import Club
from email_app.send_email import send_email
from email_app.templates import ACTIVE_CONTENT, ACTIVE_SUBJECT


class ListUsers(MethodView):
    decorators = [admin_required]

    def get(self):
        users = User.query.order_by(User.is_activated).all()
        inactive_users = User.query.filter_by(is_activated=False).count()
        if inactive_users == 1:
            flash("Vous avez 1 compte utilisateur en attente d'activation !", "warning")
        if inactive_users > 1:
            flash(
                f"Vous avez {inactive_users} comptes utilisateur en attente d'activation !",
                "warning",
            )

        return render_template("list_users.html", users=users)


class CreateUser(MethodView):
    decorators = [admin_required]

    def get(self):
        form = CreateUserForm()

        return render_template("user_form.html", form=form)

    def post(self):
        form = CreateUserForm()
        if form.validate_on_submit():
            user = User(
                role=form.role.data,
                first_name=form.first_name.data.capitalize(),
                last_name=form.last_name.data.capitalize(),
                birthdate=form.birthdate.data,
                email=form.email.data.lower(),
            )
            user.create()

            user.set_password(form.password.data)

            if form.image.data:
                user.resize_and_save_image(form.image.data)

            send_email(
                to=user.email,
                subject=ACTIVE_SUBJECT,
                content=ACTIVE_CONTENT.format(user.first_name),
            )

            flash(f"Compte utilisateur '{user.email}' créé avec succès !", "success")

            return redirect(url_for("authentication_app_admin.list_users"))

        return render_template("user_form.html", form=form)


class UpdateUser(MethodView):
    decorators = [admin_required]

    def get(self, id):
        user = User.query.get(id)
        form = UpdateUserForm(obj=user)

        return render_template("user_form.html", form=form, user=user)

    def post(self, id):
        user = User.query.get(id)
        form = UpdateUserForm(obj=user)
        if user and form.validate_on_submit():
            used_email = User.query.filter_by(email=form.email.data.lower()).first()
            if user.email != form.email.data.lower() and used_email:
                form.email.errors.append(
                    "Cet e-mail est déjà utilisé par un utilisateur !"
                )
            else:
                user.role = form.role.data
                user.first_name = form.first_name.data.capitalize()
                user.last_name = form.last_name.data.capitalize()
                user.birthdate = form.birthdate.data
                user.email = form.email.data.lower()
                user.save()

                flash(
                    f"Le compte utilisateur '{user.email}' a été mis à jour avec succès !",
                    "success",
                )

                return redirect(url_for("authentication_app_admin.list_users"))

        return render_template("user_form.html", form=form, user=user)


class ActivateDeactivateUser(MethodView):
    decorators = [admin_required]

    def get(self, id):
        user = User.query.get(id)

        if user:
            if user.is_activated:
                user.is_activated = False
                flash(
                    f"Le compte utilisateur '{user.email}' a été désactivé avec succès !",
                    "success",
                )
            else:
                user.is_activated = True
                flash(
                    f"Le compte utilisateur '{user.email}' a été activé avec succès !",
                    "success",
                )
                send_email(
                    to=user.email,
                    subject=ACTIVE_SUBJECT,
                    content=ACTIVE_CONTENT.format(user.first_name),
                )
            user.save()

            return redirect(url_for("authentication_app_admin.list_users"))


class DeleteUserConfirmation(MethodView):
    decorators = [admin_required]

    def get(self, id):
        user = User.query.get(id)

        return render_template("delete_user_confirmation.html", user=user)


class DeleteUser(MethodView):
    decorators = [admin_required]

    def get(self, id):
        user = User.query.get(id)
        user_club = Club.query.filter_by(secretary_id=user.id).first()
        email = user.email

        # case when the deleted user is assigned to a club as a secretary
        if user_club:
            user_club.secretary_id = None
            user_club.save()

        # case when the admin delete another user account
        if user and user.id != current_user.id:
            user.delete()
            flash(
                f"Le compte utilisateur '{email}' a été supprimé avec succès !",
                "success",
            )

            return redirect(url_for("authentication_app_admin.list_users"))

        # case when the admin delete his own account
        if user and user.id == current_user.id:
            user.delete()
            logout_user()
            flash("Votre compte utilisateur a été supprimé.", "info")

            return redirect(url_for("authentication_app_public.login"))
