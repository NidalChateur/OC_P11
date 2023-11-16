from flask import Blueprint

from ..views.public import ListClubs

club_app_public = Blueprint(
    "club_app_public",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)


club_app_public.add_url_rule("/", view_func=ListClubs.as_view("list_clubs"))
