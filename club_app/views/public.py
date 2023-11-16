from flask import render_template
from flask.views import MethodView

from ..models.club import Club


class ListClubs(MethodView):
    def get(self):
        clubs = Club.query.filter_by(is_activated=True)

        return render_template("list_clubs.html", clubs=clubs)
