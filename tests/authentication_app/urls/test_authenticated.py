from flask import url_for

from authentication_app.views.authenticated import (
    AddMyPhoto,
    ChangeMyPassword,
    DeleteMyAccount,
    DeleteMyAccountConfirmation,
    DeleteMyPhoto,
    MyProfile,
    UpdateMyProfile,
)


class Test_User_Urls_Authenticated:
    def test_my_profile_url(self, app):
        # 1. path check
        endpoint = url_for("authentication_app_authenticated.my_profile")
        assert endpoint == "/users/my-profile/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match("/users/my-profile/")
        assert view_name == "authentication_app_authenticated.my_profile"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == MyProfile

    def test_update_my_profile_url(self, app):
        # 1. path check
        endpoint = url_for("authentication_app_authenticated.update_my_profile")
        assert endpoint == "/users/my-profile/update/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match("/users/my-profile/update/")
        assert view_name == "authentication_app_authenticated.update_my_profile"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == UpdateMyProfile

    def test_add_my_photo_url(self, app):
        # 1. path check
        endpoint = url_for("authentication_app_authenticated.add_my_photo")
        assert endpoint == "/users/my-profile/add-my-photo/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match(
            "/users/my-profile/add-my-photo/"
        )
        assert view_name == "authentication_app_authenticated.add_my_photo"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == AddMyPhoto

    def test_delete_my_photo_url(self, app):
        # 1. path check
        endpoint = url_for("authentication_app_authenticated.delete_my_photo")
        assert endpoint == "/users/my-profile/delete-my-photo/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match(
            "/users/my-profile/delete-my-photo/"
        )
        assert view_name == "authentication_app_authenticated.delete_my_photo"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == DeleteMyPhoto

    def test_delete_my_account_confirmation_url(self, app):
        # 1. path check
        endpoint = url_for(
            "authentication_app_authenticated.delete_my_account_confirmation"
        )
        assert endpoint == "/users/my-profile/delete-confirmation/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match(
            "/users/my-profile/delete-confirmation/"
        )
        assert (
            view_name
            == "authentication_app_authenticated.delete_my_account_confirmation"
        )

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == DeleteMyAccountConfirmation

    def test_delete_my_account_url(self, app):
        # 1. path check
        endpoint = url_for("authentication_app_authenticated.delete_my_account")
        assert endpoint == "/users/my-profile/delete/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match("/users/my-profile/delete/")
        assert view_name == "authentication_app_authenticated.delete_my_account"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == DeleteMyAccount

    def test_change_my_password_url(self, app):
        # 1. path check
        endpoint = url_for("authentication_app_authenticated.change_my_password")
        assert endpoint == "/users/my-profile/change-my-password/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match(
            "/users/my-profile/change-my-password/"
        )
        assert view_name == "authentication_app_authenticated.change_my_password"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == ChangeMyPassword
