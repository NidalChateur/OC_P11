import pytest
from sqlalchemy.exc import IntegrityError

from authentication_app.models.user import User, db
from club_app.models.club import Club


class TestClub:
    def _clear_club_table(self, app):
        [club.delete() for club in Club.query.all()]

    def _create_club_instance(self, app) -> Club:
        club_test = Club(secretary_id=1, name="club_test")

        return club_test

    def test_str_rpr_club(self, app):
        self._clear_club_table(app)

        club = self._create_club_instance(app)
        club.id = 1

        club_id = f"id : {club.id}"
        secretary_name = f"nom du secrétaire : {club.secretary_name}"
        club_name = f"nom du club : {club.name}"
        club_points = f"points : {club.points}"

        assert str(club) == f"{club_id}, {secretary_name}, {club_name}, {club_points}"

        assert str(club) == repr(club)

    def test_email_property(self, app):
        # 1. test a club with a secretary
        club_with_secretary = self._create_club_instance(app)
        secretary = db.session.get(User, club_with_secretary.secretary_id)

        assert club_with_secretary.email == secretary.email

        # 2. test a club without secretary
        club_without_secretary = Club(secretary_id=None, name="club_test_2")

        assert club_without_secretary.email == ""

    def test_secretary_name_property(self, app):
        # 1. test a club with a secretary
        club_with_secretary = self._create_club_instance(app)
        secretary = db.session.get(User, club_with_secretary.secretary_id)

        assert (
            club_with_secretary.secretary_name
            == f"{secretary.first_name} {secretary.last_name}"
        )

        # 2. test a club without secretary
        club_without_secretary = Club(secretary_id=None, name="club_test_2")

        assert club_without_secretary.secretary_name == ""

    def test_validate_secretary_id(self, app):
        non_existent_secretary = db.session.get(User, 0)

        assert non_existent_secretary is None

        with pytest.raises(ValueError, match="L'id de ce secrétaire n'existe pas !"):
            Club(secretary_id=0, name="club_test")

    @pytest.mark.parametrize(
        "points, error_message",
        [
            ("-5", "Le nombre de point doit être de type int !"),
            (-2, "Le nombre de point ne peut être inférieur à 0 !"),
        ],
    )
    def test_validate_points(self, app, points, error_message):
        with pytest.raises(ValueError, match=error_message):
            Club(secretary_id=1, name="club_test", points=points)

    def test_name_unicity(self, app):
        club_1 = Club(secretary_id=None, name="club")
        club_1.create()

        with pytest.raises(IntegrityError):
            club_2 = Club(secretary_id=None, name="club")
            club_2.create()

        # rollback the last mistaken commit "competition_2.create()"
        db.session.rollback()

        club_1.delete()

    def test_init_db(self, app):
        club_1 = Club.query.filter_by(
            secretary_id=2, name="Simply Lift", points=13
        ).first()

        assert club_1 is None

        club_2 = Club.query.filter_by(
            secretary_id=3, name="Iron Temple", points=4
        ).first()

        assert club_2 is None

        club_3 = Club.query.filter_by(
            secretary_id=4, name="She Lifts", points=12
        ).first()

        assert club_3 is None

        Club.init_db()

        club_1 = Club.query.filter_by(
            secretary_id=2, name="Simply Lift", points=13
        ).first()

        assert club_1 is not None

        club_2 = Club.query.filter_by(
            secretary_id=3, name="Iron Temple", points=4
        ).first()

        assert club_2 is not None

        club_3 = Club.query.filter_by(
            secretary_id=4, name="She Lifts", points=12
        ).first()

        assert club_3 is not None
