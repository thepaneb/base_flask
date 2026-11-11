"""Schemas (marshmallow) do módulo hello_world: query params e resposta."""

import marshmallow as ma


class HelloQuerySchema(ma.Schema):
    """Query params aceitos: `name` e `lang` (ambos opcionais)."""

    name = ma.fields.Str(required=False, load_default=None, metadata={"example": "Ana"})
    lang = ma.fields.Str(required=False, load_default=None, metadata={"example": "pt"})


class HelloSchema(ma.Schema):
    """Formato da resposta de saudação."""

    message = ma.fields.Str(required=True, metadata={"example": "Olá, Ana!"})
    timestamp = ma.fields.Str(required=True)
