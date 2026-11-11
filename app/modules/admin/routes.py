"""Rotas do módulo admin (camada fina: HTTP + service + resposta)."""

from flask import Response, current_app, render_template
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from .schemas import AdminStatsSchema, CacheClearSchema
from .service import clear_cache, get_stats

bp = Blueprint("admin", __name__, description="Operação (requer JWT)")


@bp.get("/")
@bp.response(200, AdminStatsSchema)
@jwt_required()
@bp.doc(security=[{"bearerAuth": []}])
def stats():
    """Resumo operacional: contagens, uptime e versão."""
    return get_stats(current_app.config["API_VERSION"])


@bp.get("/dashboard")
@jwt_required()
@bp.doc(security=[{"bearerAuth": []}])
def dashboard():
    """Painel HTML simples (exemplo de template server-side; fora do @response)."""
    html = render_template(
        "admin/dashboard.html", stats=get_stats(current_app.config["API_VERSION"])
    )
    return Response(html, mimetype="text/html")


@bp.post("/cache/clear")
@bp.response(200, CacheClearSchema)
@jwt_required()
@bp.doc(security=[{"bearerAuth": []}])
def cache_clear():
    """Limpa todo o cache da aplicação (requer JWT)."""
    clear_cache()
    return {"cleared": True}
