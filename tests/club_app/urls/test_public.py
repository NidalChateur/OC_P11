from flask import url_for

from club_app.views.public import ListClubs


class Test_Club_Urls_Public:
    def test_list_clubs_url(self, app):
        # 1. path check
        endpoint = url_for("club_app_public.list_clubs")
        assert endpoint == "/"

        # # 2. view_name check
        view_name, _ = app.url_map.bind("localhost").match("/")
        assert view_name == "club_app_public.list_clubs"

        # 3. view_class check
        view_class = app.view_functions[view_name].view_class
        assert view_class == ListClubs
