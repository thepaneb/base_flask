"""Schemas (marshmallow) do módulo visits."""

import marshmallow as ma


class VisitCreateSchema(ma.Schema):
    """Corpo do POST /visits."""

    name = ma.fields.Str(required=False, load_default=None, metadata={"example": "Ada"})


class VisitListQuerySchema(ma.Schema):
    """Filtros do GET /visits (combinam com a paginação do smorest)."""

    name = ma.fields.Str(required=False, load_default=None, metadata={"example": "Ada"})
    order = ma.fields.Str(
        required=False, load_default="desc", validate=ma.validate.OneOf(["asc", "desc"])
    )


class VisitSchema(ma.Schema):
    """Uma visita registrada."""

    id = ma.fields.Int(required=True)
    name = ma.fields.Str(required=True)
    created_at = ma.fields.DateTime(required=True)
