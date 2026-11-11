"""Fixtures compartilhadas (app isolado por teste, banco em memória)."""

import pytest

from app import create_app
from app.config import TestingConfig
from app.extensions import db


@pytest.fixture()
def client():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
