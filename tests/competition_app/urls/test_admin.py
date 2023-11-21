import pytest
from flask import url_for

from competition_app.views.admin import (
    CreateCompetition,
    DeleteCompetition,
    DeleteCompetitionConfirmation,
    DeleteReservation,
    DeleteReservationConfirmation,
    ListCompetitions,
    ListReservations,
)


class Test_Competition_Urls_Admin:
    @pytest.mark.parametrize(
        "endpoint, url_name, class_name",
        [
            (
                "/admin/competitions/",
                "competition_app_admin.list_competitions",
                ListCompetitions,
            ),
            (
                "/admin/competitions/create/",
                "competition_app_admin.create_competition",
                CreateCompetition,
            ),
            (
                "/admin/competitions/<int:id>/delete-confirmation/",
                "competition_app_admin.delete_competition_confirmation",
                DeleteCompetitionConfirmation,
            ),
            (
                "/admin/competitions/<int:id>/delete/",
                "competition_app_admin.delete_competition",
                DeleteCompetition,
            ),
            (
                "/admin/reservations/",
                "competition_app_admin.list_reservations",
                ListReservations,
            ),
            (
                "/admin/reservations/<int:id>/delete-confirmation/",
                "competition_app_admin.delete_reservation_confirmation",
                DeleteReservationConfirmation,
            ),
            (
                "/admin/reservations/<int:id>/delete/",
                "competition_app_admin.delete_reservation",
                DeleteReservation,
            ),
        ],
    )
    def test_admin_urls(self, app, endpoint, url_name, class_name):
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
