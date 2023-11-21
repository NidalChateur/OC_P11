# create an app environnement for testing

import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app("config.Testing")

    with app.app_context():
        yield app


@pytest.fixture
def client():
    """used to test post an get requests"""

    app = create_app("config.Testing")

    with app.app_context():
        with app.test_client() as client:
            yield client
