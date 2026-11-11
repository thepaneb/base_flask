"""Schemas (marshmallow) do módulo visits."""

import marshmallow as ma


class VisitCreateSchema(ma.Schema):
    """Corpo do POST /visits."""

    name = ma.fields.Str(required=False, load_default=None)


class VisitSchema(ma.Schema):
    """Uma visita registrada."""

    id = ma.fields.Int(required=True)
    name = ma.fields.Str(required=True)
    created_at = ma.fields.DateTime(required=True)
