"""Fixtures compartilhadas (app isolado por teste, banco em memória)."""

import pytest

from app import create_app
from app.config import TestingConfig


@pytest.fixture()
def client():
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client
