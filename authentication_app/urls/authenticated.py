from flask import Blueprint

from authentication_app.views.authenticated import (
    AddMyPhoto,
    ChangeMyPassword,
    DeleteMyAccount,
    DeleteMyAccountConfirmation,
    DeleteMyPhoto,
    MyProfile,
    UpdateMyProfile,
)

authentication_app_authenticated = Blueprint(
    "authentication_app_authenticated",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)


authentication_app_authenticated.add_url_rule(
    "/users/my-profile/",
    view_func=MyProfile.as_view("my_profile"),
)
authentication_app_authenticated.add_url_rule(
    "/users/my-profile/update/",
    view_func=UpdateMyProfile.as_view("update_my_profile"),
)
authentication_app_authenticated.add_url_rule(
    "/users/my-profile/add-my-photo/",
    view_func=AddMyPhoto.as_view("add_my_photo"),
)
authentication_app_authenticated.add_url_rule(
    "/users/my-profile/delete-my-photo/",
    view_func=DeleteMyPhoto.as_view("delete_my_photo"),
)
authentication_app_authenticated.add_url_rule(
    "/users/my-profile/delete-confirmation/",
    view_func=DeleteMyAccountConfirmation.as_view("delete_my_account_confirmation"),
)
authentication_app_authenticated.add_url_rule(
    "/users/my-profile/delete/",
    view_func=DeleteMyAccount.as_view("delete_my_account"),
)
authentication_app_authenticated.add_url_rule(
    "/users/my-profile/change-my-password/",
    view_func=ChangeMyPassword.as_view("change_my_password"),
)
