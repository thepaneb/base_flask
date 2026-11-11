"""Regra de negócio do módulo visits (pura: sem `flask`, sem banco direto)."""

from .repository import VisitRepository

_repository = VisitRepository()


def record_visit(name, repository=None):
    """Valida e registra uma visita. Nome vazio vira "anonymous"."""
    repo = repository or _repository
    clean = name.strip() if name and name.strip() else "anonymous"
    return repo.add(clean)


def list_visits(page=1, page_size=10, name=None, order="desc", repository=None):
    """Retorna (itens, total) da página pedida."""
    repo = repository or _repository
    offset = (page - 1) * page_size
    return repo.list(limit=page_size, offset=offset, name=name, order=order), repo.count(name=name)


def get_visit(visit_id, repository=None):
    """Retorna uma visita pelo id (None se não existir)."""
    return (repository or _repository).get(visit_id)


def delete_visit(visit_id, repository=None):
    """Remove uma visita. Retorna False se não existir."""
    repo = repository or _repository
    visit = repo.get(visit_id)
    if visit is None:
        return False
    repo.delete(visit)
    return True
