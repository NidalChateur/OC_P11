import pytest
from flask import url_for

from club_app.views.authenticated import (
    CreateMyClub,
    DeleteMyClub,
    DeleteMyClubConfirmation,
    MyClub,
    UpdateMyClub,
)


class Test_Club_Urls_Authenticated:
    @pytest.mark.parametrize(
        "endpoint, url_name, class_name",
        [
            (
                "/clubs/my-club/",
                "club_app_authenticated.my_club",
                MyClub,
            ),
            (
                "/clubs/my-club/create/",
                "club_app_authenticated.create_my_club",
                CreateMyClub,
            ),
            (
                "/clubs/my-club/update/",
                "club_app_authenticated.update_my_club",
                UpdateMyClub,
            ),
            (
                "/clubs/my-club/delete-confirmation/",
                "club_app_authenticated.delete_my_club_confirmation",
                DeleteMyClubConfirmation,
            ),
            (
                "/clubs/my-club/delete/",
                "club_app_authenticated.delete_my_club",
                DeleteMyClub,
            ),
        ],
    )
    def test_authenticated_urls(self, app, endpoint, url_name, class_name):
        # 1. path check
        assert url_for(url_name) == endpoint

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match(endpoint)
        assert view_name == url_name

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == class_name
