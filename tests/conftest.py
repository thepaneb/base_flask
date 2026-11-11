"""Fixtures compartilhadas (app isolado por teste, banco em memória)."""

import pytest
from flask_migrate import upgrade

from app import create_app
from app.config import TestingConfig
from app.extensions import cache


@pytest.fixture()
def client():
    app = create_app(TestingConfig)
    with app.app_context():
        upgrade()  # schema real via migrations (nunca create_all no runtime)
        cache.clear()
    with app.test_client() as client:
        yield client


@pytest.fixture()
def auth_headers(client):
    """Registra um usuário e devolve o header Authorization com access token."""
    client.post("/v1/auth/register", json={"username": "ada", "password": "s3cret"})
    tokens = client.post(
        "/v1/auth/login", json={"username": "ada", "password": "s3cret"}
    ).get_json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}
