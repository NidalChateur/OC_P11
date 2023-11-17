# from competition_app.models.club import Club

from datetime import datetime

from sqlalchemy.orm import validates

from authentication_app.models import CrudMixin, db
from authentication_app.models.user import User


class Club(db.Model, CrudMixin):
    id = db.Column(db.Integer, primary_key=True)

    secretary_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=True, unique=True
    )
    name = db.Column(db.String(128), nullable=False, unique=True)
    points = db.Column(db.Integer, default=10, nullable=False)

    is_activated = db.Column(db.Boolean, default=True)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, secretary_id: int, name: str, points=10):
        self.secretary_id = secretary_id
        self.name = name
        self.points = points

    def __str__(self) -> str:
        club_id = f"id : {self.id}"
        secretary_name = f"nom du secrétaire : {self.secretary_name}"
        club_name = f"nom du club : {self.name}"
        club_points = f"points : {self.points}"

        return f"{club_id}, {secretary_name}, {club_name}, {club_points}"

    def __repr__(self) -> str:
        return str(self)

    @property
    def email(self):
        if self.secretary_id:
            secretary = User.query.get(self.secretary_id)

            return secretary.email

        return ""

    @property
    def secretary_name(self):
        if self.secretary_id:
            secretary = User.query.get(self.secretary_id)

            return f"{secretary.first_name} {secretary.last_name}"

        return ""

    @validates("secretary_id")
    def validate_secretary_id(self, key, value):
        if value:
            secretary = User.query.get(value)
            if not secretary:
                raise ValueError("L'id de ce secrétaire n'existe pas !")

        return value

    @validates("points")
    def validate_points(self, key, value):
        if not isinstance(value, int):
            raise ValueError("Le nombre de point doit être de type int !")

        if value < 0:
            raise ValueError("Le nombre de point ne peut être < 0 !")

        return value

    @staticmethod
    def init_db():
        club_1 = Club(secretary_id=2, name="Simply Lift", points=13)
        club_1.create()

        club_2 = Club(secretary_id=3, name="Iron Temple", points=4)
        club_2.create()

        club_3 = Club(secretary_id=4, name="She Lifts", points=12)
        club_3.create()
