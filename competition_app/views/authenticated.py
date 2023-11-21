from flask import flash, redirect, render_template, url_for
from flask.views import MethodView
from flask_login import current_user, login_required

from club_app.models.club import Club

from ..forms.authenticated import CreateReservationForm
from ..models.competition import Competition, Reservation


class ListCompetitions(MethodView):
    decorators = [login_required]

    def get(self):
        competitions = Competition.query.order_by(Competition.start_date.desc()).all()
        club = Club.query.filter_by(secretary_id=current_user.id).first()
        if not club:
            flash(
                "Vous devez avoir enregistré votre club pour effectuer une réservation ! ",
                "warning",
            )

            return render_template(
                "list_competitions.html", competitions=competitions, club=False
            )

        return render_template(
            "list_competitions.html", competitions=competitions, club=club
        )


class ListReservations(MethodView):
    decorators = [login_required]

    def get(self):
        club = Club.query.filter_by(secretary_id=current_user.id).first()
        if club:
            reservations = (
                Reservation.query.filter_by(club_id=club.id)
                .order_by(Reservation.competition_id)
                .all()
            )
        else:
            reservations = []

        return render_template(
            "list_reservations.html", reservations=reservations, club=club
        )


class CreateReservation(MethodView):
    decorators = [login_required]

    def get(self, id):
        form = CreateReservationForm()
        club = Club.query.filter_by(secretary_id=current_user.id).first()
        competition = Competition.query.get(id)
        reservation = Reservation.query.filter_by(
            club_id=club.id, competition_id=competition.id
        ).first()

        if not club:
            """ if current_user has no club """

            return redirect(url_for("competition_app_authenticated.list_competitions"))

        if not competition:
            """ if the competition does not exists """

            flash("Aucune compétition trouvée !", "error")

            return redirect(url_for("competition_app_authenticated.list_competitions"))

        if reservation:
            flash(
                "Votre club ne peut réaliser qu'une réservation par compétition !",
                "error",
            )
            return redirect(url_for("competition_app_authenticated.list_competitions"))

        return render_template(
            "competition_form.html", form=form, club=club, competition=competition
        )

    def post(self, id):
        form = CreateReservationForm()
        club = Club.query.filter_by(secretary_id=current_user.id).first()
        competition = Competition.query.get(id)
        reservation = Reservation.query.filter_by(
            club_id=club.id, competition_id=competition.id
        ).first()

        if not club:
            return redirect(url_for("competition_app_authenticated.list_competitions"))

        if not competition:
            flash("Aucune compétition trouvée !", "error")

            return redirect(url_for("competition_app_authenticated.list_competitions"))

        if reservation:
            flash(
                "Votre club ne peut réaliser qu'une réservation par compétition !",
                "error",
            )

            return redirect(url_for("competition_app_authenticated.list_competitions"))

        if form.validate_on_submit():
            entered_number = form.number_of_spots.data

            if entered_number > int(club.points):
                form.number_of_spots.errors.append(
                    f"Votre club possède {club.points} point(s)..."
                )

            elif entered_number > competition.remaining_spots:
                form.number_of_spots.errors.append(
                    f"Il ne reste plus que {competition.remaining_spots} place(s) dans cette compétition..."
                )

            else:
                club.points -= entered_number
                club.save()
                reservation = Reservation(
                    club_id=club.id,
                    competition_id=competition.id,
                    number_of_spots=entered_number,
                )
                reservation.create()
                flash(
                    f"Réservation de {entered_number} place(s) dans la compétition {competition.name}.",
                    "success",
                )
                return redirect(
                    url_for("competition_app_authenticated.list_competitions")
                )

        return render_template(
            "competition_form.html", form=form, club=club, competition=competition
        )


class DeleteReservationConfirmation(MethodView):
    decorators = [login_required]

    def get(self, id):
        reservation = Reservation.query.get(id)
        if reservation:
            return render_template(
                "delete_reservation_confirmation.html",
                reservation=reservation,
                delete_from_my_reservation=True,
            )


class DeleteReservation(MethodView):
    decorators = [login_required]

    def get(self, id):
        reservation = Reservation.query.get(id)
        club = Club.query.filter_by(secretary_id=current_user.id).first()

        if not reservation:
            flash("Aucune réservation trouvée !", "error")

            return redirect(url_for("competition_app_authenticated.list_reservations"))

        if not club:
            flash("Vous n'avez pas club !", "error")

            return redirect(url_for("competition_app_authenticated.list_reservations"))

        if not reservation.is_cancelable:
            flash(
                "Cette réservation n'est pas annulable car la date de compétition est passée !",
                "error",
            )

            return redirect(url_for("competition_app_authenticated.list_reservations"))

        competition_name = reservation.competition_name
        recovered_points = reservation.number_of_spots
        reservation.delete()
        club.points += recovered_points
        club.save()

        flash(
            f"La réservation effectuée sur la compétition '{competition_name}' a été supprimé avec succès",
            "success",
        )

        flash(
            f"Votre club '{club.name}' a récupéré {recovered_points} point(s).", "info"
        )

        return redirect(url_for("competition_app_authenticated.list_reservations"))
