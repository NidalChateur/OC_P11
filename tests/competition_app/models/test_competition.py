import sqlite3
from datetime import date, datetime, timedelta

import pytest
from flask import g
from sqlalchemy.exc import IntegrityError

from authentication_app.models.user import User, db
from club_app.models.club import Club
from competition_app.models.competition import (
    Competition,
    Reservation,
    delete_club_reservations,
)
from config import Testing


def start_date() -> datetime:
    return datetime.utcnow() + timedelta(days=14)


class Test_Delete_Club_Reservation:
    def test_delete_club_reservations(self, app):
        """Plan test :
        1. retrieving an existing club from db
        2. creating 2 competitions in db
        3. creating 1 reservation for each competition
        4. deleting all club reservation
        5. clearing db"""

        # 1. retrieving an existing club from db
        club = Club.query.filter_by(name="Simply Lift").first()

        # 2. creating 2 competitions in db
        competition_1 = Competition(
            name="Competition 1 test club", start_date=start_date()
        )
        competition_1.create()

        competition_2 = Competition(
            name="Competition 2 test club", start_date=start_date()
        )
        competition_2.create()

        # 3. creating 1 reservation for each competition
        reservation_1 = Reservation(club_id=club.id, competition_id=competition_1.id)
        reservation_1.create()

        reservation_2 = Reservation(club_id=club.id, competition_id=competition_2.id)
        reservation_2.create()

        assert Reservation.query.filter_by(club_id=club.id).count() > 0

        # 4. deleting all club reservation
        delete_club_reservations(club_id=club.id)

        assert Reservation.query.filter_by(club_id=club.id).count() == 0

        # 5. clearing db
        competition_1.delete()
        competition_2.delete()


class TestCompetition:
    def _clear_duplicate(self, app):
        user = User.query.filter_by(
            email="competition_test@competition_test.com"
        ).first()
        if user:
            user.delete()

        club = Club.query.filter_by(name="club test competition").first()
        if club:
            delete_club_reservations(club.id)
            club.delete()

        competitions = Competition.query.all()
        for competition in competitions:
            competition.delete_reservations()
            competition.delete()

    def _create_user_instance(self, app) -> User:
        user_test = User(
            role="secretary",
            first_name="first_name",
            last_name="last_name",
            birthdate=date(year=2000, month=1, day=1),
            email="competition_test@competition_test.com",
        )

        return user_test

    def _create_club_instance(self, app, secretary_id=None) -> Club:
        club_test = Club(secretary_id=secretary_id, name="club test competition")

        return club_test

    def _create_competition_instance(self, app) -> Competition:
        test_competition = Competition(name="Competition test", start_date=start_date())

        return test_competition

    def test_str_rpr(self, app):
        self._clear_duplicate(app)

        competition = self._create_competition_instance(app)
        competition.id = 1

        competition_id = f"id : {competition.id}"
        competition_name = f"nom de compétition : {competition.name}"
        competition_date = f"date : {competition.start_date_formatter}"
        competition_capacity = f"capacité : {competition.capacity}"

        assert (
            str(competition)
            == f"{competition_id}, {competition_name}, {competition_date}, {competition_capacity}"
        )

        assert str(competition) == repr(competition)

    def test_start_date_formatter_property(self, app):
        competition = self._create_competition_instance(app)

        assert competition.start_date_formatter == competition.start_date.strftime(
            "%d/%m/%Y à %Hh%M"
        )

    def test_has_started_property(self, app):
        competition = self._create_competition_instance(app)

        assert isinstance(competition.has_started, bool)
        assert isinstance(competition.start_date > datetime.utcnow(), bool)

        assert competition.has_started is not (
            competition.start_date > datetime.utcnow()
        )

    def test_remaining_spots_property(self, app):
        secretary = self._create_user_instance(app)
        secretary.create()

        club = self._create_club_instance(app, secretary_id=secretary.id)
        club.create()

        competition = self._create_competition_instance(app)
        competition.create()

        # 1. test with no reservation
        assert competition.remaining_spots == competition.capacity

        reservation = Reservation(
            club_id=club.id, competition_id=competition.id, number_of_spots=club.points
        )
        reservation.create()

        # 2. test with a reservation
        assert (
            competition.remaining_spots
            == competition.capacity - reservation.number_of_spots
        )

    def test_is_full_property(self, app):
        competition = Competition.query.filter_by(name="Competition test").first()

        assert isinstance(competition.is_full, bool)
        assert isinstance(competition.remaining_spots > 0, bool)
        assert competition.is_full is not (competition.remaining_spots > 0)

    def test_delete_reservations(self, app):
        # 1. test whether reservations exist for a competition
        competition = Competition.query.filter_by(name="Competition test").first()

        reservations_number = Reservation.query.filter_by(
            competition_id=competition.id
        ).count()

        assert competition is not None
        assert reservations_number > 0

        # 2. test whether reservations have been deleted for a competition
        competition.delete_reservations()

        reservations_number = Reservation.query.filter_by(
            competition_id=competition.id
        ).count()

        assert reservations_number == 0

    @pytest.mark.parametrize(
        "capacity, error_message",
        [
            ("55", "La capacité doit être de type int !"),
            (-1, "La capacité ne peut être inférieur à 0 !"),
        ],
    )
    def test_validate_capacity(self, app, capacity, error_message):
        with pytest.raises(ValueError, match=error_message):
            Competition(
                name="competition test capacity",
                start_date=start_date(),
                capacity=capacity,
            )

    @pytest.mark.parametrize(
        "start_date, error_message",
        [
            ("11/11/2024 à 9h00", "La date de début doit être de type datetime !"),
            (
                datetime(year=2023, month=11, day=20),
                "Le début de la compétition ne doit pas commencer avant 7 jours !",
            ),
        ],
    )
    def test_validate_start_date(self, app, start_date, error_message):
        with pytest.raises(ValueError, match=error_message):
            Competition(
                name="competition test start_date",
                start_date=start_date,
            )

    def test_name_unicity(self, app):
        competition_1 = Competition(name="competition", start_date=start_date())
        competition_1.create()

        with pytest.raises(IntegrityError):
            competition_2 = Competition(name="competition", start_date=start_date())
            competition_2.create()

        # rollback the last mistaken commit "competition_2.create()"
        db.session.rollback()

        competition_1.delete()

    def test_init_db(self, app):
        competition_1 = Competition.query.filter_by(
            name="Spring Festival",
            start_date=datetime(year=2024, month=3, day=27, hour=10),
            capacity=25,
        ).first()

        assert competition_1 is None

        competition_2 = Competition.query.filter_by(
            name="Fall Classic",
            start_date=datetime(year=2024, month=10, day=22, hour=13, minute=30),
            capacity=13,
        ).first()

        assert competition_2 is None

        Competition.init_db()

        competition_1 = Competition.query.filter_by(
            name="Spring Festival",
            start_date=datetime(year=2024, month=3, day=27, hour=10),
            capacity=25,
        ).first()

        assert competition_1 is not None

        competition_2 = Competition.query.filter_by(
            name="Fall Classic",
            start_date=datetime(year=2024, month=10, day=22, hour=13, minute=30),
            capacity=13,
        ).first()

        assert competition_2 is not None


class TestReservation:
    def _retrieve_club(self, app, club_name: str) -> Club:
        return Club.query.filter_by(name=club_name).first()

    def _retrieve_competition(self, app, competition_name: str) -> Competition:
        return Competition.query.filter_by(name=competition_name).first()

    def _create_reservation_instance(self, app) -> Reservation:
        club = self._retrieve_club(app, "Simply Lift")
        competition = self._retrieve_competition(app, "Spring Festival")

        return Reservation(club_id=club.id, competition_id=competition.id)

    def test_str_rpr(self, app):
        reservation = self._create_reservation_instance(app)
        reservation.id = 1

        reservation_id = f"id : {reservation.id}"
        club_name = f"nom du club : {reservation.club_name}"
        competition_name = f"nom de compétition : {reservation.competition_name}"
        number_of_spots = f"places : {reservation.number_of_spots}"

        assert (
            str(reservation)
            == f"{reservation_id}, {club_name}, {competition_name}, {number_of_spots}"
        )

        assert str(reservation) == repr(reservation)

    def test_is_cancelable_property(self, app):
        reservation = self._create_reservation_instance(app)
        competition = db.session.get(Competition, reservation.competition_id)

        assert isinstance(reservation.is_cancelable, bool)
        assert isinstance(competition.has_started, bool)
        assert reservation.is_cancelable is not competition.has_started

    def test_club_name_property(self, app):
        reservation = self._create_reservation_instance(app)
        club = db.session.get(Club, reservation.club_id)

        assert reservation.club_name is not None
        assert isinstance(reservation.club_name, str)

        assert club.name is not None
        assert isinstance(club.name, str)

        assert reservation.club_name == club.name

    def test_competition_name_property(self, app):
        reservation = self._create_reservation_instance(app)
        competition = db.session.get(Competition, reservation.competition_id)

        assert reservation.competition_name is not None
        assert isinstance(reservation.competition_name, str)

        assert competition.name is not None
        assert isinstance(competition.name, str)

        assert reservation.competition_name == competition.name

    @pytest.mark.parametrize(
        "number_of_spots, error_message",
        [
            ("5", "Le nombre de place doit être de type int !"),
            (0, "Le nombre de place ne peut être inférieur à 1 !"),
            (13, "Le nombre de place ne peut être supérieur à 12 !"),
        ],
    )
    def test_validate_number_of_spots(self, app, number_of_spots, error_message):
        club = self._retrieve_club(app, "Simply Lift")
        competition = self._retrieve_competition(app, "Spring Festival")

        with pytest.raises(ValueError, match=error_message):
            Reservation(
                club_id=club.id,
                competition_id=competition.id,
                number_of_spots=number_of_spots,
            )

    @pytest.mark.parametrize(
        "club_id, error_message",
        [
            ("5", "L'id du club doit être de type int !"),
            (0, "L'id de ce club n'existe pas !"),
            (
                "create a club without secretary",
                "Pour réserver le club doit avoir un secrétaire !",
            ),
        ],
    )
    def test_validate_club_id(self, app, club_id, error_message):
        competition = self._retrieve_competition(app, "Spring Festival")

        if club_id == "create a club without secretary":
            club = Club(secretary_id=None, name="club without secretary")
            club.create()
            # club = self._retrieve_club(app, "club without secretary")

        with pytest.raises(ValueError, match=error_message):
            if club_id == "create a club without secretary":
                Reservation(
                    club_id=club.id,
                    competition_id=competition.id,
                )
                club.delete()

            else:
                Reservation(
                    club_id=club_id,
                    competition_id=competition.id,
                )
        if club_id == "create a club without secretary":
            club.delete()

    def _get_db(app):
        if "db" not in g:
            g.db = sqlite3.connect(Testing.DATABASE)
            g.db.row_factory = sqlite3.Row
        return g.db

    def _insert_past_competition(self, app):
        """create a past competition without sqlalchemy but using SQL
        allow to avoid Competition.validate_start_date"""

        db = self._get_db()
        created_time = datetime.utcnow()
        start_date = datetime.utcnow() - timedelta(days=14)
        db.execute(
            "INSERT INTO competition (name, start_date, capacity, created_time) VALUES (?, ?, ?, ?)",
            ("past competition", start_date, 50, created_time),
        )
        db.commit()

    def _insert_competition_with_zero_capacity(self, app):
        """create a competition without sqlalchemy but using SQL
        allow to avoid Competition.validate_number_of_spots"""

        db = self._get_db()
        created_time = datetime.utcnow()
        db.execute(
            "INSERT INTO competition (name, start_date, capacity, created_time) VALUES (?, ?, ?, ?)",
            ("competition with 0 capacity", start_date(), 0, created_time),
        )
        db.commit()

    @pytest.mark.parametrize(
        "competition_id, error_message",
        [
            ("5", "L'id de la compétition doit être de type int !"),
            (0, "L'id de cette compétition n'existe pas !"),
            ("past", "Il faut réserver avant la date de début de compétition !"),
            ("0", "Plus de place disponible dans cette compétition !"),
        ],
    )
    def test_validate_competition_id(self, app, competition_id, error_message):
        club = self._retrieve_club(app, "Simply Lift")

        if competition_id == "past":
            self._insert_past_competition(app)
            competition = Competition.query.filter_by(name="past competition").first()

        if competition_id == "0":
            self._insert_competition_with_zero_capacity(app)
            competition = Competition.query.filter_by(
                name="competition with 0 capacity"
            ).first()

        with pytest.raises(ValueError, match=error_message):
            if competition_id == "past" or competition_id == "0":
                Reservation(club_id=club.id, competition_id=competition.id)

            else:
                Reservation(club_id=club.id, competition_id=competition_id)

        if competition_id == "past" or competition_id == "0":
            competition.delete()

    def test_unique_club_reservation_by_competition(self, app):
        reservation_1 = db.session.get(Reservation, 1)
        club = db.session.get(Club, reservation_1.club_id)
        competition = db.session.get(Competition, reservation_1.competition_id)

        with pytest.raises(IntegrityError):
            reservation_2 = Reservation(club_id=club.id, competition_id=competition.id)
            reservation_2.create()

        # rollback the last mistaken commit "reservation_2.create()"
        db.session.rollback()

        reservation_1.delete()
