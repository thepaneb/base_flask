"""Regra de negócio do módulo admin (pura: sem `flask`, sem banco direto)."""

import time

from app.modules.auth.repository import UserRepository
from app.modules.visits.repository import VisitRepository

_started_at = time.monotonic()


def get_stats(version, users=None, visits=None):
    """Monta o resumo operacional (contagens + uptime + versão)."""
    users_repo = users or UserRepository()
    visits_repo = visits or VisitRepository()
    return {
        "users_total": users_repo.count(),
        "visits_total": visits_repo.count(),
        "uptime_seconds": round(time.monotonic() - _started_at, 1),
        "version": version,
    }
