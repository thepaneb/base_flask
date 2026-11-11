"""Regra de negócio do módulo visits (pura: sem `flask`, sem banco direto)."""

from .repository import VisitRepository

_repository = VisitRepository()


def record_visit(name, repository=None):
    """Valida e registra uma visita. Nome vazio vira "anonymous"."""
    repo = repository or _repository
    clean = name.strip() if name and name.strip() else "anonymous"
    return repo.add(clean)


def list_visits(repository=None):
    """Retorna as visitas registradas."""
    return (repository or _repository).list_all()
