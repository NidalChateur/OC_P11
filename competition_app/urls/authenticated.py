from flask import Blueprint

from ..views.authenticated import (
    CreateReservation,
    DeleteReservation,
    DeleteReservationConfirmation,
    ListCompetitions,
    ListReservations,
)

competition_app_authenticated = Blueprint(
    "competition_app_authenticated",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)

competition_app_authenticated.add_url_rule(
    "/competitions/", view_func=ListCompetitions.as_view("list_competitions")
)
competition_app_authenticated.add_url_rule(
    "/reservations/", view_func=ListReservations.as_view("list_reservations")
)
competition_app_authenticated.add_url_rule(
    "/reservations/<int:id>/create/",
    view_func=CreateReservation.as_view("create_reservation"),
)
competition_app_authenticated.add_url_rule(
    "/reservations/<int:id>/delete-confirmation/",
    view_func=DeleteReservationConfirmation.as_view("delete_reservation_confirmation"),
)
competition_app_authenticated.add_url_rule(
    "/reservations/<int:id>/delete/",
    view_func=DeleteReservation.as_view("delete_reservation"),
)
