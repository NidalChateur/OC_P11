import pytest

from . import (
    cancel_club_reservation,
    club,
    create_competition_with_one_place,
    create_full_competition,
    create_past_competition,
    db_is_up_to_date,
    get_a_reservable_competition,
    get_all_reservable_competitions,
    get_club_reservation,
    is_a_reservable_competition,
    login,
    logout,
)


class Test_ListCompetitions:
    def _get(self, client):
        """make a GET request on the path : '/competitions/' and return the response"""

        return client.get(
            "/competitions/",
            follow_redirects=True,
        )

    def test_get_without_login(self, client):
        """test the GET method of ListCompetitions view without authentication
        test should redirect to login view"""

        assert logout(client)

        response = self._get(client)

        assert response.status_code == 200
        assert "Connexion" in response.data.decode()

    def test_get_with_login(self, client):
        """test the GET method of ListCompetitions view with authentication"""

        assert login(client)

        response = self._get(client)

        assert response.status_code == 200
        assert "Liste des compétitions" in response.data.decode()

    def test_get_reservable_competitions(self, client):
        """check the presence of all reservable competitions
        for an authenticated secretary"""

        # 1. login
        assert login(client)

        # 2. retrieving from db all reservable competitions
        competitions = get_all_reservable_competitions()
        assert len(competitions) > 0

        # 3. get "/competitions/"
        response = self._get(client)

        # 4. testing for the presence of "coming competitions"
        assert "Liste des compétitions" in response.data.decode()
        for competition in competitions:
            assert competition.name in response.data.decode()

    def test_get_past_competitions(self, client):
        """check the absence of past competition
        for an authenticated secretary"""

        # 1. creating a past competition in db
        competition = create_past_competition()

        assert competition.has_started

        # 2. login
        assert login(client)

        # 3. get "/competitions/"
        response = self._get(client)

        # 4. testing for the absence of "past competition"
        assert "Liste des compétitions" in response.data.decode()
        assert competition.name not in response.data.decode()

    def test_get_full_competitions(self, client):
        """check the absence of full competition
        for an authenticated secretary"""

        # 1. creating a full competition in db
        competition = create_full_competition()

        assert competition.is_full

        # 2. login
        assert login(client)

        # 3. get "/competitions/"
        response = self._get(client)

        # 4. testing for the absence of "full competition"
        assert "Liste des compétitions" in response.data.decode()
        assert competition.name not in response.data.decode()


class Test_CreateReservation:
    """testing GET method"""

    def _get(self, client, competition_id: int):
        """make a GET request on the path : '/reservations/<int:id>/create/'
        return the response"""

        return client.get(
            f"/reservations/{competition_id}/create/",
            follow_redirects=True,
        )

    def test_get_without_login(self, client):
        """Plan test :
        1. getting a reservable competition id from db
        2. logout
        3. trying a get request without being authenticated"""

        # 1. getting a reservable competition id from db
        competition = get_a_reservable_competition()

        assert is_a_reservable_competition(competition)

        # 2. logout
        assert logout(client)

        # 3. trying a get request without being authenticated
        response = self._get(client, competition.id)

        assert response.status_code == 200
        assert "Connexion" in response.data.decode()

    def test_get_with_login(self, client):
        """Plan test :
        1. getting a reservable competition id from db
        2. login
        3. trying a get request being authenticated"""

        # 1. getting a reservable competition id from db
        competition = get_a_reservable_competition()

        assert is_a_reservable_competition(competition)

        # 2. login
        assert login(client)

        # 3. trying a get request being authenticated
        response = self._get(client, competition.id)

        assert response.status_code == 200
        assert "Réserver des places dans la compétition" in response.data.decode()

    def test_get_with_a_past_competition(self, client):
        """Plan test :
        1. getting a a past competition from db
        2. login
        3. trying a get request with a past competition id"""

        # 1. getting a past competition from db
        competition = create_past_competition()

        assert competition.has_started

        # 2. login
        assert login(client)

        # 3. trying a get request being authenticated
        response = self._get(client, competition.id)

        assert response.status_code == 200
        assert "Permission refusée !" in response.data.decode()
        assert "Liste des compétitions" in response.data.decode()

    def test_get_with_a_full_competition(self, client):
        """Plan test :
        1. getting a a full competition from db
        2. login
        3. trying a get request with a full competition id"""

        # 1. getting a full competition from db
        competition = create_full_competition()

        assert competition.is_full

        # 2. login
        assert login(client)

        # 3. trying a get request being authenticated
        response = self._get(client, competition.id)

        assert response.status_code == 200
        assert "Permission refusée !" in response.data.decode()
        assert "Liste des compétitions" in response.data.decode()

    """testing POST method"""

    def _post(self, client, competition_id: int, number_of_spots: int):
        return client.post(
            f"/reservations/{competition_id}/create/",
            json={"number_of_spots": number_of_spots},
            follow_redirects=True,
        )

    def test_post_without_login(self, client):
        """Plan test :
        1. getting a reservable competition id from db
        2. logout
        3. trying a post request without being authenticated"""

        # 1. getting a reservable competition id from db
        competition = get_a_reservable_competition()

        assert is_a_reservable_competition(competition)

        # 2. logout
        assert logout(client)

        # 3. trying a post request without being authenticated
        number_of_spots = 1

        response = self._post(
            client,
            competition_id=competition.id,
            number_of_spots=number_of_spots,
        )

        assert response.status_code == 200
        assert "Connexion" in response.data.decode()

    def test_post_with_login(self, client):
        """Plan test :
        1. getting a reservable competition id from db
        2. login
        3. trying a post request being authenticated
        4. checking db is up to date after reservation"""

        # 1. getting a reservable competition id from db
        competition = get_a_reservable_competition()

        assert is_a_reservable_competition(competition)

        remaining_spots_capture = competition.remaining_spots

        # 2. login
        assert login(client)

        club_points_capture = club().points

        # 3. trying a post request without being authenticated
        number_of_spots = 1

        response = self._post(
            client,
            competition_id=competition.id,
            number_of_spots=number_of_spots,
        )

        assert response.status_code == 200
        assert "Liste des compétitions" in response.data.decode()
        assert "Réservation réussie !" in response.data.decode()

        # 4. checking db is up to date after reservation
        reservation = get_club_reservation(competition)

        assert db_is_up_to_date(
            club_points_before_reservation=club_points_capture,
            remaining_spots_before_reservation=remaining_spots_capture,
            competition=competition,
            reservation=reservation,
        )

        cancel_club_reservation(number_of_spots)

    @pytest.mark.parametrize(
        "number_of_spots, error_message",
        [
            (13, "Number must be between 1 and 12."),
            (12, "Votre club possède 4 point(s)..."),
            (4, "Il ne reste plus que 1 place(s) dans cette compétition..."),
        ],
    )
    def test_post_with_an_over_value(self, client, number_of_spots, error_message):
        """Plan test :
        1. getting a reservable competition id from db
        2. login
        3. trying a post request being authenticated
        4. checking reservation is not created in db"""

        # 1. getting a reservable competition id from db
        if error_message == "Il ne reste plus que 1 place(s) dans cette compétition...":
            competition = create_competition_with_one_place()
        else:
            competition = get_a_reservable_competition()

        assert is_a_reservable_competition(competition)

        # 2. login
        assert login(client)

        # 3. trying a post request without being authenticated

        response = self._post(
            client,
            competition_id=competition.id,
            number_of_spots=number_of_spots,
        )

        assert response.status_code == 200
        assert "Réserver des places dans la compétition" in response.data.decode()
        assert error_message in response.data.decode()

        # 4. checking reservation is not created in db
        reservation = get_club_reservation(competition)

        assert reservation is None

    @pytest.mark.parametrize(
        "type_of_competition",
        [
            ("past"),
            ("full"),
        ],
    )
    def test_post_with_past_then_full_competition(self, client, type_of_competition):
        """Plan test :
        1. getting a past then a full competition from db
        2. login
        3. trying a post request with a past then a full competition
        4. checking reservation is not created in db
        """

        # 1. getting a past then a full competition from db
        if type_of_competition == "past":
            competition = create_past_competition()
            assert competition.has_started
        else:
            competition = create_full_competition()
            assert competition.is_full

        # 2. login
        assert login(client)

        # 3. trying a post request with a past then a full competition
        response = self._post(
            client,
            competition_id=competition.id,
            number_of_spots=1,
        )

        assert response.status_code == 200
        assert "Permission refusée !" in response.data.decode()
        assert "Liste des compétitions" in response.data.decode()

        # 4. checking reservation is not created in db
        reservation = get_club_reservation(competition)

        assert reservation is None
