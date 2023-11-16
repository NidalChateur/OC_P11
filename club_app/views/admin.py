from flask import flash, redirect, render_template, url_for
from flask.views import MethodView

from authentication_app.decorator import admin_required
from authentication_app.models.user import User
from competition_app.models.competition import delete_club_reservations

from ..forms.admin import CreateClubForm, UpdateClubForm
from ..models.club import Club


class ListClubs(MethodView):
    decorators = [admin_required]

    def get(self):
        clubs = Club.query.order_by(Club.is_activated).all()
        inactive_clubs = Club.query.filter_by(is_activated=False).count()
        if inactive_clubs == 1:
            flash("Vous avez 1 club en attente d'activation !", "warning")
        if inactive_clubs > 1:
            flash(
                f"Vous avez {inactive_clubs} clubs en attente d'activation !" "warning",
            )

        return render_template("list_clubs.html", clubs=clubs)


class CreateClub(MethodView):
    decorators = [admin_required]

    def get(self):
        form = CreateClubForm()

        return render_template("club_form.html", form=form)

    def post(self):
        form = CreateClubForm()
        if form.validate_on_submit():
            secretary = User.query.filter_by(email=form.email.data.lower()).first()
            club = Club(
                secretary_id=secretary.id,
                name=form.name.data.title(),
                points=form.points.data,
            )
            club.create()

            flash(f"Le club {club.name} a été créé avec succès !", "success")

            return redirect(url_for("club_app_admin.list_clubs"))

        return render_template("club_form.html", form=form)


class UpdateClub(MethodView):
    decorators = [admin_required]

    def get(self, id):
        club = Club.query.get(id)
        form = UpdateClubForm(obj=club)

        return render_template("club_form.html", form=form, club=club)

    def post(self, id):
        club = Club.query.get(id)
        form = UpdateClubForm(obj=club)
        if club and form.validate_on_submit():
            is_a_used_club_name = Club.query.filter_by(
                name=form.name.data.title()
            ).first()

            secretary = User.query.filter_by(email=form.email.data.lower()).first()
            if secretary:
                secretary_has_a_club = Club.query.filter_by(
                    secretary_id=secretary.id
                ).first()
            else:
                secretary_has_a_club = False

            if club.email != form.email.data.lower() and secretary_has_a_club:
                form.email.errors.append("Ce secrétaire est déjà assigné à un club !")

            elif club.name != form.name.data.title() and is_a_used_club_name:
                form.name.errors.append("Ce nom de club est déjà utilisé !")

            else:
                if secretary:
                    club.secretary_id = secretary.id

                else:
                    club.secretary_id = None

                club.name = form.name.data.title()
                club.points = form.points.data
                club.save()

                flash(
                    f"Le club '{club.name}' a été mis à jour avec succès !", "success"
                )

                return redirect(url_for("club_app_admin.list_clubs"))

        return render_template("club_form.html", form=form, club=club)


class ActivateDeactivateClub(MethodView):
    decorators = [admin_required]

    def get(self, id):
        club = Club.query.get(id)
        if club:
            if club.is_activated:
                club.is_activated = False
                flash(f"Le club '{club.name}' a été désactivé avec succès !", "success")

            else:
                club.is_activated = True
                flash(f"Le club '{club.name}' a été activé avec succès !", "success")

            club.save()

            return redirect(url_for("club_app_admin.list_clubs"))


class DeleteClubConfirmation(MethodView):
    decorators = [admin_required]

    def get(self, id):
        club = Club.query.get(id)

        return render_template("delete_club_confirmation.html", club=club)


class DeleteClub(MethodView):
    decorators = [admin_required]

    def get(self, id):
        club = Club.query.get(id)

        if club:
            club_name = club.name
            delete_club_reservations(club_id=club.id)
            club.delete()
            flash(f"Le club '{club_name}' a été supprimé avec succès !", "success")

            return redirect(url_for("club_app_admin.list_clubs"))
