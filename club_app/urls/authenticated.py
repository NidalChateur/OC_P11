from flask import Blueprint

from ..views.authenticated import (
    CreateMyClub,
    DeleteMyClub,
    DeleteMyClubConfirmation,
    MyClub,
    UpdateMyClub,
)

club_app_authenticated = Blueprint(
    "club_app_authenticated",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)

club_app_authenticated.add_url_rule(
    "/clubs/my-club/", view_func=MyClub.as_view("my_club")
)
club_app_authenticated.add_url_rule(
    "/clubs/my-club/create/", view_func=CreateMyClub.as_view("create_my_club")
)
club_app_authenticated.add_url_rule(
    "/clubs/my-club/update/", view_func=UpdateMyClub.as_view("update_my_club")
)
club_app_authenticated.add_url_rule(
    "/clubs/my-club/delete-confirmation/",
    view_func=DeleteMyClubConfirmation.as_view("delete_my_club_confirmation"),
)
club_app_authenticated.add_url_rule(
    "/clubs/my-club/delete/",
    view_func=DeleteMyClub.as_view("delete_my_club"),
)
