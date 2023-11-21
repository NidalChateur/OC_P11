import pytest
from flask import url_for

from club_app.views.admin import (
    ActivateDeactivateClub,
    CreateClub,
    DeleteClub,
    DeleteClubConfirmation,
    ListClubs,
    UpdateClub,
)


class Test_Club_Urls_Admin:
    @pytest.mark.parametrize(
        "endpoint, url_name, class_name",
        [
            (
                "/admin/clubs/",
                "club_app_admin.list_clubs",
                ListClubs,
            ),
            (
                "/admin/clubs/create/",
                "club_app_admin.create_club",
                CreateClub,
            ),
            (
                "/admin/clubs/<int:id>/activate-deactivate/",
                "club_app_admin.activate_deactivate_club",
                ActivateDeactivateClub,
            ),
            (
                "/admin/clubs/<int:id>/update/",
                "club_app_admin.update_club",
                UpdateClub,
            ),
            (
                "/admin/clubs/<int:id>/delete-confirmation/",
                "club_app_admin.delete_club_confirmation",
                DeleteClubConfirmation,
            ),
            (
                "/admin/clubs/<int:id>/delete/",
                "club_app_admin.delete_club",
                DeleteClub,
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
