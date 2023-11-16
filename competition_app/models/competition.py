from datetime import datetime, timedelta

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from authentication_app.models import CrudMixin, db
from club_app.models.club import Club


def delete_club_reservations(club_id: int):
    """all club reservations will be deleted, used in DeleteClub views"""

    club_reservations = Reservation.query.filter_by(club_id=club_id).all()

    if club_reservations:
        for reservation in club_reservations:
            reservation.delete()


class Competition(db.Model, CrudMixin):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=False, unique=True)
    start_date = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, default=50, nullable=False)

    created_time = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, name: str, start_date: datetime, capacity=50):
        self.name = name
        self.start_date = start_date
        self.capacity = capacity

    def __str__(self) -> str:
        competition_id = f"id : {self.id}"
        competition_name = f"nom de compétition : {self.name}"
        competition_date = f"date : {self.start_date_formatter}"
        competition_capacity = f"capacité : {self.capacity}"

        return f"{competition_id}, {competition_name}, {competition_date}, {competition_capacity}"

    def __repr__(self) -> str:
        return str(self)

    @property
    def start_date_formatter(self) -> str:
        return self.start_date.strftime("%d/%m/%Y à %Hh%M")

    @property
    def has_started(self) -> bool:
        if self.start_date > datetime.utcnow():
            return False
        return True

    @property
    def remaining_spots(self) -> int:
        reserved_spots = (
            db.session.query(func.sum(Reservation.number_of_spots))
            .filter_by(competition_id=self.id)
            .scalar()
            or 0
        )

        return self.capacity - reserved_spots

    @property
    def is_full(self) -> bool:
        if self.remaining_spots > 0:
            return False

        return True

    def delete_reservations(self):
        """all competition reservations will be deleted"""

        competition_reservations = Reservation.query.filter_by(
            competition_id=self.id
        ).all()

        if competition_reservations:
            for reservation in competition_reservations:
                db.session.delete(reservation)

    @validates("capacity")
    def validate_capacity(self, key, value):
        if not isinstance(value, int):
            raise ValueError("La capacité (nombre de place) doit être de type int !")

        if value < 1:
            raise ValueError("La capacité (nombre de place) ne peut être < 1 !")

        return value

    @validates("start_date")
    def validate_start_date(self, key, value):
        if value < datetime.utcnow() + timedelta(days=7):
            raise ValueError(
                "Le début de la compétition ne doit pas commencer avant 7 jours !"
            )

        return value

    @staticmethod
    def init_db():
        competition_1 = Competition(
            name="Spring Festival",
            start_date=datetime(year=2024, month=3, day=27, hour=10),
            capacity=25,
        )
        competition_1.create()

        competition_2 = Competition(
            name="Fall Classic",
            start_date=datetime(year=2024, month=10, day=22, hour=13, minute=30),
            capacity=13,
        )
        competition_2.create()


class Reservation(db.Model, CrudMixin):
    id = db.Column(db.Integer, primary_key=True)

    number_of_spots = db.Column(db.Integer, default=5, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"), nullable=False)
    competition_id = db.Column(
        db.Integer, db.ForeignKey("competition.id"), nullable=False
    )

    created_time = db.Column(db.DateTime, default=datetime.utcnow())

    __table_args__ = (
        UniqueConstraint(
            "club_id", "competition_id", name="unique_club_reservation_by_competition"
        ),
    )

    def __init__(self, club_id: int, competition_id: int, number_of_spots=5):
        self.club_id = club_id
        self.competition_id = competition_id
        self.number_of_spots = number_of_spots

    def __str__(self) -> str:
        reservation_id = f"id : {self.id}"
        club_name = f"nom du club : {self.club_name}"
        competition_name = f"nom de compétition : {self.competition_name}"
        number_of_spots = f"places : {self.number_of_spots}"

        return f"{reservation_id}, {club_name}, {competition_name}, {number_of_spots}"

    def __repr__(self) -> str:
        return str(self)

    @property
    def is_cancelable(self) -> bool:
        competition = Competition.query.get(self.competition_id)

        return not competition.has_started

    @property
    def club_name(self) -> bool:
        club = Club.query.get(self.club_id)

        return club.name

    @property
    def competition_name(self) -> bool:
        competition = Competition.query.get(self.competition_id)

        return competition.name

    @validates("number_of_spots")
    def validate_number_of_spots(self, key, value):
        if not isinstance(value, int):
            raise ValueError("Le nombre de place doit être de type int !")

        if value < 1:
            raise ValueError("Le nombre de place ne peut être < 1 !")

        if value > 12:
            raise ValueError("Le nombre de place ne peut être > 12 !")

        return value

    @validates("club_id")
    def validate_club_id(self, key, value):
        if not isinstance(value, int):
            raise ValueError("L'id du club doit être de type int !")

        club = Club.query.get(value)

        if not club:
            raise ValueError("L'id de ce club n'existe pas !")

        if club.points == 0:
            raise ValueError("Le club ne possède plus de point !")

        return value

    @validates("competition_id")
    def validate_competition_id(self, key, value):
        if not isinstance(value, int):
            raise ValueError("Le nombre de place doit être de type int !")

        competition = Competition.query.get(value)
        if not competition:
            raise ValueError("L'id de cette compétition n'existe pas !")

        if competition.has_started:
            raise ValueError("Il faut réserver avant la date de début de compétition !")

        if competition.is_full:
            raise ValueError("Plus de place disponible dans cette compétition !")

        return value
