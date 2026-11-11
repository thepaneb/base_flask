"""Schemas (marshmallow) do módulo auth."""

import marshmallow as ma


class RegisterSchema(ma.Schema):
    """Corpo do POST /auth/register."""

    username = ma.fields.Str(required=True, metadata={"example": "ada"})
    password = ma.fields.Str(required=True, load_only=True, metadata={"example": "s3cret"})


class LoginSchema(ma.Schema):
    """Corpo do POST /auth/login."""

    username = ma.fields.Str(required=True, metadata={"example": "ada"})
    password = ma.fields.Str(required=True, load_only=True, metadata={"example": "s3cret"})


class TokenPairSchema(ma.Schema):
    """Par de tokens do login."""

    access_token = ma.fields.Str(required=True)
    refresh_token = ma.fields.Str(required=True)


class AccessTokenSchema(ma.Schema):
    """Novo par de tokens do refresh (rotação: o antigo é revogado)."""

    access_token = ma.fields.Str(required=True)
    refresh_token = ma.fields.Str(required=True)


class MessageSchema(ma.Schema):
    """Mensagem simples (ex. logout)."""

    message = ma.fields.Str(required=True)


class UserSchema(ma.Schema):
    """Usuário (nunca expõe o hash)."""

    id = ma.fields.Int(required=True)
    username = ma.fields.Str(required=True)
    created_at = ma.fields.DateTime(required=True)
