"""Regra de negócio do módulo hello_world (pura: sem `flask`, sem HTTP)."""

from .repository import DEFAULT_LANG, GreetingRepository

_repository = GreetingRepository()


def greet(name=None, lang=None, repository=None):
    """Monta a saudação. Nome vazio vira "world"; idioma desconhecido cai no padrão."""
    repo = repository or _repository
    clean_name = name.strip() if name and name.strip() else "world"
    template = repo.get_template((lang or DEFAULT_LANG).lower())
    return template.format(name=clean_name)
