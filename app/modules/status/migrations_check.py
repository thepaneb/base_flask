"""Checagem de migrations pendentes (para o readiness não servir schema velho)."""

import os

from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory


def _migrations_dir():
    # <repo>/migrations a partir deste arquivo (app/modules/<mod>/migrations_check.py)
    here = os.path.abspath(__file__)
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(here)))),
        "migrations",
    )


def check_migrations():
    """True se o banco está no head das migrations (sem pendências)."""
    from app.extensions import db

    try:
        script = ScriptDirectory(_migrations_dir())
        with db.engine.connect() as connection:
            context = MigrationContext.configure(connection)
            current = set(context.get_current_heads() or [])
        heads = set(script.get_heads())
        return bool(heads) and current == heads
    except Exception:
        return False
