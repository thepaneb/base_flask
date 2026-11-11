"""Acesso aos dados do módulo hello_world.

Hoje em memória; para persistir (DB, arquivo, i18n remoto) troque esta
classe sem tocar `service.py` nem `routes.py`.
"""

TEMPLATES = {
    "en": "Hello, {name}!",
    "pt": "Olá, {name}!",
    "es": "¡Hola, {name}!",
}

DEFAULT_LANG = "en"


class GreetingRepository:
    """Fonte dos modelos de saudação."""

    def __init__(self, templates=None):
        self._templates = dict(templates or TEMPLATES)

    def get_template(self, lang):
        """Retorna o modelo do idioma ou o padrão quando desconhecido."""
        return self._templates.get(lang, self._templates[DEFAULT_LANG])

    @property
    def supported_langs(self):
        """Idiomas disponíveis, em ordem alfabética."""
        return sorted(self._templates)
