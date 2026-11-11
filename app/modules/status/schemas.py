"""Schemas (marshmallow) do health-check e liveness."""

import marshmallow as ma


class LiveSchema(ma.Schema):
    """Resposta do liveness (processo no ar)."""

    status = ma.fields.Str(required=True)


class StatusSchema(ma.Schema):
    """Resposta do readiness (serviço + banco)."""

    status = ma.fields.Str(required=True)
    timestamp = ma.fields.Str(required=True)
    database = ma.fields.Str(required=True)
    migrations = ma.fields.Str(required=True)
