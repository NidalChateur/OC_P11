from flask import Blueprint

from authentication_app.views.admin import (
    ActivateDeactivateUser,
    CreateUser,
    DeleteUser,
    DeleteUserConfirmation,
    ListUsers,
    UpdateUser,
)

authentication_app_admin = Blueprint(
    "authentication_app_admin",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)


authentication_app_admin.add_url_rule(
    "/admin/users/",
    view_func=ListUsers.as_view("list_users"),
)
authentication_app_admin.add_url_rule(
    "/admin/users/create/",
    view_func=CreateUser.as_view("create_user"),
)
authentication_app_admin.add_url_rule(
    "/admin/users/<int:id>/update/",
    view_func=UpdateUser.as_view("update_user"),
)
authentication_app_admin.add_url_rule(
    "/admin/users/<int:id>/delete-confirmation/",
    view_func=DeleteUserConfirmation.as_view("delete_user_confirmation"),
)
authentication_app_admin.add_url_rule(
    "/admin/users/<int:id>/delete/",
    view_func=DeleteUser.as_view("delete_user"),
)
authentication_app_admin.add_url_rule(
    "/admin/users/<int:id>/activate-deactivate/",
    view_func=ActivateDeactivateUser.as_view("activate_deactivate_user"),
)
