import pytest
from flask import url_for

from competition_app.views.authenticated import (
    CreateReservation,
    DeleteReservation,
    DeleteReservationConfirmation,
    ListCompetitions,
    ListReservations,
)


class Test_Competition_Urls_Authenticated:
    @pytest.mark.parametrize(
        "endpoint, url_name, class_name",
        [
            (
                "/competitions/",
                "competition_app_authenticated.list_competitions",
                ListCompetitions,
            ),
            (
                "/reservations/",
                "competition_app_authenticated.list_reservations",
                ListReservations,
            ),
            (
                "/reservations/<int:id>/create",
                "competition_app_authenticated.create_reservation",
                CreateReservation,
            ),
            (
                "/reservations/<int:id>/delete-confirmation/",
                "competition_app_authenticated.delete_reservation_confirmation",
                DeleteReservationConfirmation,
            ),
            (
                "/reservations/<int:id>/delete/",
                "competition_app_authenticated.delete_reservation",
                DeleteReservation,
            ),
        ],
    )
    def test_authenticated_urls(self, app, endpoint, url_name, class_name):
        # 1. path check
        if "id" in endpoint:
            endpoint = endpoint.replace("<int:id>", str(1))
            assert url_for(url_name, id=1) == endpoint
        else:
            assert url_for(url_name) == endpoint

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match(endpoint)
        assert view_name == url_name

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == class_name
