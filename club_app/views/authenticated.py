from flask import flash, redirect, render_template, url_for
from flask.views import MethodView
from flask_login import current_user, login_required

from competition_app.models.competition import delete_club_reservations

from ..forms.authenticated import CreateClubForm, UpdateClubForm
from ..models.club import Club


class MyClub(MethodView):
    decorators = [login_required]

    def get(self):
        club = Club.query.filter_by(secretary_id=current_user.id).first()
        if club and not club.is_activated:
            flash(
                "Votre club a été désactivé par l'admin, contactez le pour plus d'information.",
                "warning",
            )

        return render_template("my_club.html", club=club)


class CreateMyClub(MethodView):
    decorators = [login_required]

    def get(self):
        form = CreateClubForm()

        return render_template("club_form.html", form=form)

    def post(self):
        form = CreateClubForm()
        if form.validate_on_submit():
            club = Club(
                secretary_id=current_user.id,
                name=form.name.data.title(),
            )
            club.create()

            flash(f"Le club {club.name} a été créé avec succès !", "success")

            return redirect(url_for("club_app_authenticated.my_club"))

        return render_template("club_form.html", form=form)


class UpdateMyClub(MethodView):
    decorators = [login_required]

    def get(self):
        club = Club.query.filter_by(secretary_id=current_user.id).first()
        form = UpdateClubForm(obj=club)

        return render_template("club_form.html", form=form, club=club)

    def post(self):
        club = Club.query.filter_by(secretary_id=current_user.id).first()
        form = UpdateClubForm(obj=club)

        if club and form.validate_on_submit():
            is_a_used_club_name = Club.query.filter_by(
                name=form.name.data.title()
            ).first()

            if club.name != form.name.data.title() and is_a_used_club_name:
                form.name.errors.append("Ce nom de club est déjà utilisé !")

            else:
                club.name = form.name.data.title()
                club.save()

                flash(
                    f"Le club '{club.name}' a été mis à jour avec succès !", "success"
                )

                return redirect(url_for("club_app_authenticated.my_club"))

        return render_template("club_form.html", form=form, club=club)


class DeleteMyClubConfirmation(MethodView):
    decorators = [login_required]

    def get(self):
        club = Club.query.filter_by(secretary_id=current_user.id).first()

        return render_template(
            "delete_club_confirmation.html", club=club, delete_from_my_club_profile=True
        )


class DeleteMyClub(MethodView):
    decorators = [login_required]

    def get(self):
        club = Club.query.filter_by(secretary_id=current_user.id).first()

        if club:
            club_name = club.name
            delete_club_reservations(club_id=club.id)
            club.delete()
            flash(f"Le club '{club_name}' a été supprimé avec succès !", "success")

            return redirect(url_for("club_app_authenticated.my_club"))
