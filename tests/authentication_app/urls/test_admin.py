import pytest
from flask import url_for

from authentication_app.views.admin import (
    ActivateDeactivateUser,
    CreateUser,
    DeleteUser,
    DeleteUserConfirmation,
    ListUsers,
    UpdateUser,
)


class Test_User_Urls_Admin:
    @pytest.mark.parametrize(
        "endpoint, url_name, class_name",
        [
            (
                "/admin/users/",
                "authentication_app_admin.list_users",
                ListUsers,
            ),
            (
                "/admin/users/create/",
                "authentication_app_admin.create_user",
                CreateUser,
            ),
            (
                "/admin/users/<int:id>/update/",
                "authentication_app_admin.update_user",
                UpdateUser,
            ),
            (
                "/admin/users/<int:id>/delete-confirmation/",
                "authentication_app_admin.delete_user_confirmation",
                DeleteUserConfirmation,
            ),
            (
                "/admin/users/<int:id>/delete/",
                "authentication_app_admin.delete_user",
                DeleteUser,
            ),
            (
                "/admin/users/<int:id>/activate_deactivate/",
                "authentication_app_admin.activate_deactivate_user",
                ActivateDeactivateUser,
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
