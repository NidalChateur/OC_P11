import sqlite3
from datetime import datetime, timedelta

from flask import g
from flask_login import current_user

from club_app.models.club import Club
from competition_app.models.competition import (
    Competition,
    Reservation,
    delete_club_reservations,
)
from config import Testing
from tests.competition_app.models.test_competition import start_date

# club.points == 4
EMAIL = "admin@irontemple.com"
PASSWORD = "00000000pW-"


def login(client) -> bool:
    """authenticate a user to test "login_required" views
    return current_user.is_authenticated"""

    logout(client)

    client.post(
        "/login/",
        json={"email": EMAIL, "password": PASSWORD},
        follow_redirects=True,
    )

    return current_user.is_authenticated


def logout(client) -> bool:
    """logout current_user to test public views
    return not current_user.is_authenticated"""

    client.get("/logout/", follow_redirects=True)

    return not current_user.is_authenticated


def _get_db():
    if "db" not in g:
        g.db = sqlite3.connect(Testing.DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def _clean_duplicate():
    past_competition = Competition.query.filter_by(name="past competition").first()
    if past_competition:
        past_competition.delete()

    full_competition = Competition.query.filter_by(name="full competition").first()
    if full_competition:
        full_competition.delete()

    competition_one_place = Competition.query.filter_by(name="one place").first()
    if competition_one_place:
        competition_one_place.delete()


def create_past_competition() -> Competition:
    """create a past competition without sqlalchemy but using SQL
    allow to avoid Competition.validate_start_date"""

    _clean_duplicate()

    db = _get_db()
    created_time = datetime.utcnow()
    start_date = datetime.utcnow() - timedelta(days=14)
    db.execute(
        "INSERT INTO competition (name, start_date, capacity, created_time) VALUES (?, ?, ?, ?)",
        ("past competition", start_date, 50, created_time),
    )
    db.commit()

    return Competition.query.filter_by(name="past competition").first()


def create_full_competition() -> Competition:
    """create a competition without sqlalchemy but using SQL
    allow to avoid Competition.validate_number_of_spots"""

    _clean_duplicate()

    db = _get_db()
    created_time = datetime.utcnow()
    db.execute(
        "INSERT INTO competition (name, start_date, capacity, created_time) VALUES (?, ?, ?, ?)",
        ("full competition", start_date(), 0, created_time),
    )
    db.commit()

    return Competition.query.filter_by(name="full competition").first()


def create_competition_with_one_place() -> Competition:
    _clean_duplicate()
    competition = Competition("one place", start_date(), 1)
    competition.create()

    return competition


def get_a_reservable_competition() -> Competition:
    """get from db a reservable competition
    return the reservable competition"""

    return Competition.query.filter_by(name="Spring Festival").first()


def get_all_reservable_competitions() -> list[Competition]:
    """get from db all reservable_competitions"""

    all_competitions = Competition.query.all()

    return [
        competition
        for competition in all_competitions
        if is_a_reservable_competition(competition)
    ]


def is_a_reservable_competition(competition: Competition) -> bool:
    if competition and not competition.has_started and not competition.is_full:
        return True
    return False


def club() -> Club:
    """return curent_user club"""

    return Club.query.filter_by(secretary_id=current_user.id).first()


def cancel_club_reservation(number_of_spots: int):
    """restore data after test (clean)"""

    club().points += number_of_spots
    club().save()
    delete_club_reservations(club().id)


def _are_club_points_updated(
    club_points_before_reservation: int,
    reservation: Reservation,
) -> bool:
    """check if the club.points have been updated in db"""

    return club().points == club_points_before_reservation - reservation.number_of_spots


def _are_remaining_spots_updated(
    competition: Competition,
    reservation: Reservation,
    remaining_spots_before_reservation: int,
) -> bool:
    """check the competition.remaining_spots have been updated in db"""
    return (
        competition.remaining_spots
        == remaining_spots_before_reservation - reservation.number_of_spots
    )


def db_is_up_to_date(
    club_points_before_reservation: int,
    remaining_spots_before_reservation: int,
    competition: Competition,
    reservation: Reservation,
) -> bool:
    """check if db is up to date after reservation"""

    return all(
        [
            club(),
            competition,
            reservation,
            _are_club_points_updated(club_points_before_reservation, reservation),
            _are_remaining_spots_updated(
                competition, reservation, remaining_spots_before_reservation
            ),
        ]
    )


def get_club_reservation(competition: Competition) -> Reservation:
    return Reservation.query.filter_by(
        club_id=club().id, competition_id=competition.id
    ).first()
