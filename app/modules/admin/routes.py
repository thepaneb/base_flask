"""Rotas do módulo admin (camada fina: HTTP + service + resposta)."""

from flask import current_app
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from .schemas import AdminStatsSchema
from .service import get_stats

bp = Blueprint("admin", __name__, description="Operação (requer JWT)")


@bp.get("/")
@bp.response(200, AdminStatsSchema)
@jwt_required()
@bp.doc(security=[{"bearerAuth": []}])
def stats():
    """Resumo operacional: contagens, uptime e versão."""
    return get_stats(current_app.config["API_VERSION"])
