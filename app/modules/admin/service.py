"""Regra de negócio do módulo admin (compõe services; sem banco direto)."""

import time

from app.extensions import cache
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


def clear_cache():
    """Limpa todo o cache da aplicação (blocklist vive no banco: intacta)."""
    cache.clear()
    return True
