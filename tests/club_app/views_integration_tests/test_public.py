from flask_login import current_user

from tests.competition_app.views_integration_tests import logout

from . import get_all_activated_clubs


class Test_ListClubs:
    def test_get(self, client):
        # 1. check if current_user is not authenticated
        assert logout(client)

        # 2. ger '/'
        response = client.get(
            "/",
            follow_redirects=True,
        )

        # 3. response check
        assert response.status_code == 200
        assert not current_user.is_authenticated
        assert "Liste des clubs" in response.data.decode()

        for club in get_all_activated_clubs():
            assert club.name in response.data.decode()
            assert str(club.points) in response.data.decode()
