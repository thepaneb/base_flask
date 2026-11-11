"""Schema (marshmallow) do health-check."""

import marshmallow as ma


class StatusSchema(ma.Schema):
    """Formato da resposta do health-check."""

    status = ma.fields.Str(required=True)
    timestamp = ma.fields.Str(required=True)
    database = ma.fields.Str(required=True)
