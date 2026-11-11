"""Regra do health-check (a checagem do banco usa a extensão, resto é puro)."""

from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import text

from app.extensions import db


def check_database():
    """Retorna True se o banco responde a um SELECT 1."""
    try:
        db.session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def build_status(timezone):
    """Monta o payload do health-check (inclui saúde do banco)."""
    db_ok = check_database()
    return {
        "status": "ok" if db_ok else "degraded",
        "timestamp": datetime.now(ZoneInfo(timezone)).isoformat(),
        "database": "ok" if db_ok else "unreachable",
    }
