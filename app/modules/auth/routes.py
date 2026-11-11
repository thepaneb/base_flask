"""Rotas do módulo auth (camada fina: HTTP + service + resposta)."""

from flask import abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint

from app.extensions import limiter

from .repository import UserRepository
from .schemas import AccessTokenSchema, LoginSchema, RegisterSchema, TokenPairSchema, UserSchema
from .service import authenticate, register

bp = Blueprint("auth", __name__, description="Autenticação JWT")

_bearer = [{"bearerAuth": []}]


@bp.post("/register")
@bp.arguments(RegisterSchema)
@bp.response(201, UserSchema)
def register_user(args):
    """Cria um usuário. 409 se o username já existe."""
    try:
        return register(args["username"], args["password"])
    except ValueError:
        abort(409)


@bp.post("/login")
@bp.arguments(LoginSchema)
@bp.response(200, TokenPairSchema)
@limiter.limit("30 per minute")  # anti brute-force (ajuste p/ produção)
def login(args):
    """Autentica e devolve access + refresh tokens. 401 se inválido."""
    user = authenticate(args["username"], args["password"])
    if user is None:
        abort(401)
    identity = str(user.id)
    return {
        "access_token": create_access_token(identity=identity),
        "refresh_token": create_refresh_token(identity=identity),
    }


@bp.post("/refresh")
@bp.response(200, AccessTokenSchema)
@jwt_required(refresh=True)
@bp.doc(security=_bearer)
def refresh():
    """Troca um refresh token por um access token novo."""
    return {"access_token": create_access_token(identity=get_jwt_identity())}


@bp.get("/me")
@bp.response(200, UserSchema)
@jwt_required()
@bp.doc(security=_bearer)
def me():
    """Retorna o usuário do token (exemplo de rota protegida)."""
    user = UserRepository().get_by_id(int(get_jwt_identity()))
    if user is None:
        abort(401)
    return user
