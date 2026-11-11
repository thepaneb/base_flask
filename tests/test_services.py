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


class FakeVisitRepository:
    """Dublê do repository (mesma interface, sem banco)."""

    def __init__(self):
        self.items = []

    def add(self, name):
        visit = SimpleNamespace(id=len(self.items) + 1, name=name)
        self.items.append(visit)
        return visit

    def list_all(self):
        return list(self.items)


def test_record_visit_validates_and_delegates():
    repo = FakeVisitRepository()
    assert record_visit("  Ada  ", repository=repo).name == "Ada"
    assert record_visit(None, repository=repo).name == "anonymous"
    assert [v.name for v in list_visits(repository=repo)] == ["Ada", "anonymous"]
