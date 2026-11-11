"""Rota do health-check (camada fina: HTTP + service + resposta)."""

from flask import current_app
from flask_smorest import Blueprint

from .schemas import LiveSchema, StatusSchema
from .service import build_status

bp = Blueprint("status", __name__, description="Saúde do serviço")


@bp.route("/live")
@bp.response(200, LiveSchema)
def live():
    """Liveness: o processo está no ar (sem checar dependências)."""
    return {"status": "ok"}


@bp.route("/status")
@bp.response(200, StatusSchema)
def status():
    """Readiness: serviço + banco (503 se degradado)."""
    payload = build_status(current_app.config["TIMEZONE"])
    return payload, 200 if payload["status"] == "ok" else 503
