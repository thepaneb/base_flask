"""Testes do comando `flask seed`."""

from click.testing import CliRunner

from app import create_app
from app.cli import seed_command
from app.config import TestingConfig
from app.extensions import db
from app.modules.visits.models import Visit


def test_seed_command_is_idempotent():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        runner = CliRunner()
        first = runner.invoke(seed_command)
        assert first.exit_code == 0
        assert first.output.strip() == "seed: 3 visits criadas."
        second = runner.invoke(seed_command)
        assert second.output.strip() == "seed: banco já populado, nada a fazer."
        assert Visit.query.count() == 3
