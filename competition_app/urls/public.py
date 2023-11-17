from flask import Blueprint

competition_app_public = Blueprint(
    "competition_app_public",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)
