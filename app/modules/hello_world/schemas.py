"""Schemas (marshmallow) do módulo hello_world: query params e resposta."""

import marshmallow as ma


class HelloQuerySchema(ma.Schema):
    """Query params aceitos: `name` e `lang` (ambos opcionais)."""

    name = ma.fields.Str(required=False, load_default=None)
    lang = ma.fields.Str(required=False, load_default=None)


class HelloSchema(ma.Schema):
    """Formato da resposta de saudação."""

    message = ma.fields.Str(required=True)
    timestamp = ma.fields.Str(required=True)
