"""Regra do health-check (a checagem usa as extensões; o resto é puro)."""

from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import text

from app.extensions import db

from .migrations_check import check_migrations


def check_database():
    """Retorna True se o banco responde a um SELECT 1."""
    try:
        db.session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def build_status(timezone):
    """Monta o payload do health-check (banco + migrations em dia)."""
    db_ok = check_database()
    migrations_ok = check_migrations() if db_ok else False
    ok = db_ok and migrations_ok
    return {
        "status": "ok" if ok else "degraded",
        "timestamp": datetime.now(ZoneInfo(timezone)).isoformat(),
        "database": "ok" if db_ok else "unreachable",
        "migrations": "ok" if migrations_ok else "pending",
    }
