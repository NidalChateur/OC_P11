from flask import Blueprint

from ..views.admin import (
    ActivateDeactivateClub,
    CreateClub,
    DeleteClub,
    DeleteClubConfirmation,
    ListClubs,
    UpdateClub,
)

club_app_admin = Blueprint(
    "club_app_admin",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)

club_app_admin.add_url_rule("/admin/clubs/", view_func=ListClubs.as_view("list_clubs"))

club_app_admin.add_url_rule(
    "/admin/clubs/create/", view_func=CreateClub.as_view("create_club")
)

club_app_admin.add_url_rule(
    "/admin/clubs/<int:id>/activate-deactivate/",
    view_func=ActivateDeactivateClub.as_view("activate_deactivate_club"),
)

club_app_admin.add_url_rule(
    "/admin/clubs/<int:id>/update/",
    view_func=UpdateClub.as_view("update_club"),
)
club_app_admin.add_url_rule(
    "/admin/clubs/<int:id>/delete-confirmation/",
    view_func=DeleteClubConfirmation.as_view("delete_club_confirmation"),
)

club_app_admin.add_url_rule(
    "/admin/clubs/<int:id>/delete/",
    view_func=DeleteClub.as_view("delete_club"),
)
