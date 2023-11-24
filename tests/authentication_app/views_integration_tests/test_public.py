import pytest
from flask_login import current_user

from tests.competition_app.views_integration_tests import login, logout


class Test_Login:
    EMAIL = "admin@irontemple.com"
    PASSWORD = "00000000pW-"

    def test_get(self, client):
        # 1. check if current_user is not authenticated
        assert logout(client)

        # 2. get /login/
        response = client.get("/login/", follow_redirects=True)

        # 3. response check
        assert response.status_code == 200
        assert "Connexion" in response.data.decode()

    def test_post_with_valid_user_data(self, client):
        # 1. check if current_user is not authenticated
        assert logout(client)

        # 2. post /login/ with valid data
        response = client.post(
            "/login/",
            json={"email": self.EMAIL, "password": self.PASSWORD},
            follow_redirects=True,
        )

        # 3. response check
        assert response.status_code == 200
        assert current_user.is_authenticated
        assert current_user.email == self.EMAIL
        assert "Connexion réussie !" in response.data.decode()

    @pytest.mark.parametrize(
        "email, password, error_message",
        [
            (
                "unknown_email@gmail.com",
                "unknown_password",
                "Cet e-mail n&#39;est pas enregistré. Veuillez vous inscrire d&#39;abord.",
            ),
        ],
    )
    def test_post_with_invalid_user_data(self, client, email, password, error_message):
        # 1. check if current_user is not authenticated
        assert logout(client)

        # 2. post /login/ with invalid data
        response = client.post(
            "/login/",
            json={"email": email, "password": password},
            follow_redirects=True,
        )

        # 2. response check
        assert response.status_code == 200
        assert current_user.is_authenticated is False
        assert error_message in response.data.decode()


class Test_Logout:
    def test_get(self, client):
        # 1. check if current_user is authenticated
        assert login(client)

        # 2. get /logout/
        response = client.get("/logout/", follow_redirects=True)

        # 3. response check
        assert response.status_code == 200
        assert not current_user.is_authenticated
        assert "Vous êtes déconnecté." in response.data.decode()
        assert "Connexion" in response.data.decode()
