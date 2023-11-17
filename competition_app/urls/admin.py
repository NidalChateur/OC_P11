from flask import Blueprint

from ..views.admin import (
    CreateCompetition,
    DeleteCompetition,
    DeleteCompetitionConfirmation,
    DeleteReservation,
    DeleteReservationConfirmation,
    ListCompetitions,
    ListReservations,
)

competition_app_admin = Blueprint(
    "competition_app_admin",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)

competition_app_admin.add_url_rule(
    "/admin/competitions/", view_func=ListCompetitions.as_view("list_competitions")
)
competition_app_admin.add_url_rule(
    "/admin/competitions/create/",
    view_func=CreateCompetition.as_view("create_competition"),
)

competition_app_admin.add_url_rule(
    "/admin/competitions/<int:id>/delete-confirmation/",
    view_func=DeleteCompetitionConfirmation.as_view("delete_competition_confirmation"),
)
competition_app_admin.add_url_rule(
    "/admin/competitions/<int:id>/delete/",
    view_func=DeleteCompetition.as_view("delete_competition"),
)

competition_app_admin.add_url_rule(
    "/admin/reservations/", view_func=ListReservations.as_view("list_reservations")
)
competition_app_admin.add_url_rule(
    "/admin/reservations/<int:id>/delete-confirmation/",
    view_func=DeleteReservationConfirmation.as_view("delete_reservation_confirmation"),
)
competition_app_admin.add_url_rule(
    "/admin/reservations/<int:id>/delete/",
    view_func=DeleteReservation.as_view("delete_reservation"),
)
