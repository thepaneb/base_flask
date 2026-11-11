"""Schemas (marshmallow) do módulo auth."""

import marshmallow as ma


class RegisterSchema(ma.Schema):
    """Corpo do POST /auth/register."""

    username = ma.fields.Str(required=True)
    password = ma.fields.Str(required=True, load_only=True)


class LoginSchema(ma.Schema):
    """Corpo do POST /auth/login."""

    username = ma.fields.Str(required=True)
    password = ma.fields.Str(required=True, load_only=True)


class TokenPairSchema(ma.Schema):
    """Par de tokens do login."""

    access_token = ma.fields.Str(required=True)
    refresh_token = ma.fields.Str(required=True)


class AccessTokenSchema(ma.Schema):
    """Novo access token do refresh."""

    access_token = ma.fields.Str(required=True)


class UserSchema(ma.Schema):
    """Usuário (nunca expõe o hash)."""

    id = ma.fields.Int(required=True)
    username = ma.fields.Str(required=True)
    created_at = ma.fields.DateTime(required=True)
