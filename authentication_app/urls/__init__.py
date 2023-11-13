from flask import Blueprint

authentication_app = Blueprint(
    "authentication_app",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)
