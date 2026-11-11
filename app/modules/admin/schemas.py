"""Schemas (marshmallow) do módulo admin."""

import marshmallow as ma


class AdminStatsSchema(ma.Schema):
    """Resumo operacional do serviço."""

    users_total = ma.fields.Int(required=True)
    visits_total = ma.fields.Int(required=True)
    uptime_seconds = ma.fields.Float(required=True)
    version = ma.fields.Str(required=True)


class CacheClearSchema(ma.Schema):
    """Resposta da limpeza do cache."""

    cleared = ma.fields.Bool(required=True)
