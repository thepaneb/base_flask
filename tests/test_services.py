"""Testes unitários das regras de negócio (sem HTTP, sem banco)."""

from types import SimpleNamespace

from app.modules.hello_world.service import greet
from app.modules.visits.service import list_visits, record_visit


def test_greet_default():
    assert greet() == "Hello, world!"


def test_greet_with_name_and_lang():
    assert greet(name="Ana", lang="pt") == "Olá, Ana!"


def test_greet_blank_name_and_unknown_lang_fall_back():
    assert greet(name="   ", lang="xx") == "Hello, world!"


def test_supported_langs():
    from app.modules.hello_world.repository import GreetingRepository

    assert GreetingRepository().supported_langs == ["en", "es", "pt"]


class FakeVisitRepository:
    """Dublê do repository (mesma interface, sem banco)."""

    def __init__(self):
        self.items = []

    def add(self, name):
        visit = SimpleNamespace(id=len(self.items) + 1, name=name)
        self.items.append(visit)
        return visit

    def get(self, visit_id):
        return next((v for v in self.items if v.id == visit_id), None)

    def delete(self, visit):
        self.items.remove(visit)

    def list(self, limit, offset, name=None, order="desc"):
        items = [v for v in self.items if not name or name.lower() in v.name.lower()]
        items = sorted(items, key=lambda v: v.id, reverse=(order != "asc"))
        return items[offset : offset + limit]

    def count(self, name=None):
        return len([v for v in self.items if not name or name.lower() in v.name.lower()])


def test_record_visit_validates_and_delegates():
    repo = FakeVisitRepository()
    assert record_visit("  Ada  ", repository=repo).name == "Ada"
    assert record_visit(None, repository=repo).name == "anonymous"
    items, total = list_visits(repository=repo)
    assert [v.name for v in items] == ["anonymous", "Ada"]  # id desc
    assert total == 2


def test_get_and_delete_visit():
    from app.modules.visits.service import delete_visit, get_visit

    repo = FakeVisitRepository()
    visit = record_visit("Ada", repository=repo)
    assert get_visit(visit.id, repository=repo).name == "Ada"
    assert get_visit(999, repository=repo) is None
    assert delete_visit(visit.id, repository=repo) is True
    assert delete_visit(visit.id, repository=repo) is False
