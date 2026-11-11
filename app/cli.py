"""Comandos flask extras (ex.: `flask --app app seed`)."""

import click
from flask.cli import with_appcontext


@click.command("seed")
@with_appcontext
def seed_command():
    """Popula o banco com dados de exemplo (idempotente para o template)."""
    from app.modules.visits.service import list_visits, record_visit

    _, total = list_visits()
    if total == 0:
        for name in ("Ada", "Grace", "Katherine"):
            record_visit(name)
        click.echo("seed: 3 visits criadas.")
    else:
        click.echo("seed: banco já populado, nada a fazer.")
