from datetime import datetime

from flask import flash, redirect, render_template, url_for
from flask.views import MethodView

from authentication_app.decorator import admin_required
from club_app.models.club import Club, db

from ..forms.admin import CreateCompetitionForm
from ..models.competition import Competition, Reservation


class ListCompetitions(MethodView):
    decorators = [admin_required]

    def get(self):
        competitions = Competition.query.order_by(Competition.start_date.desc()).all()

        return render_template("list_competitions.html", competitions=competitions)


class CreateCompetition(MethodView):
    decorators = [admin_required]

    def get(self):
        form = CreateCompetitionForm()

        return render_template("competition_form.html", form=form)

    def post(self):
        form = CreateCompetitionForm()
        if form.validate_on_submit():
            competition = Competition(
                name=form.name.data.title(),
                start_date=datetime.combine(form.start_date.data, form.start_hour.data),
                capacity=form.capacity.data,
            )
            competition.create()
            flash(
                f"La compétition '{competition.name}' a été crée avec succès", "success"
            )

            return redirect(url_for("competition_app_admin.list_competitions"))

        return render_template("competition_form.html", form=form)


class DeleteCompetitionConfirmation(MethodView):
    decorators = [admin_required]

    def get(self, id):
        competition = Competition.query.get(id)
        if competition:
            return render_template(
                "delete_competition_confirmation.html", competition=competition
            )


class DeleteCompetition(MethodView):
    decorators = [admin_required]

    def get(self, id):
        competition = Competition.query.get(id)
        if competition:
            competition_name = competition.name
            competition.delete_reservations()
            competition.delete()

            flash(
                f"La compétition '{competition_name}' a été supprimé avec succès",
                "success",
            )

            return redirect(url_for("competition_app_admin.list_competitions"))


class ListReservations(MethodView):
    decorators = [admin_required]

    def get(self):
        reservations = Reservation.query.order_by(Reservation.competition_id).all()

        return render_template("list_reservations.html", reservations=reservations)


class DeleteReservationConfirmation(MethodView):
    decorators = [admin_required]

    def get(self, id):
        reservation = Reservation.query.get(id)
        if reservation:
            return render_template(
                "delete_reservation_confirmation.html", reservation=reservation
            )


class DeleteReservation(MethodView):
    decorators = [admin_required]

    def get(self, id):
        reservation = Reservation.query.get(id)
        if reservation:
            reservation_id = reservation.id
            club = db.session.get(Club, reservation.club_id)
            if reservation.is_cancelable and club:
                club.points += reservation.number_of_spots
                club.save()
            reservation.delete()

            flash(
                f"La réservation n°{reservation_id} a été supprimé avec succès",
                "success",
            )

            return redirect(url_for("competition_app_admin.list_reservations"))
