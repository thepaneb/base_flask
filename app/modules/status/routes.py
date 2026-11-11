"""Rota do health-check (camada fina: HTTP + service + resposta)."""

from flask import current_app, jsonify
from flask_smorest import Blueprint

from .schemas import StatusSchema
from .service import build_status

bp = Blueprint("status", __name__, description="Saúde do serviço")


@bp.route("/status")
@bp.response(200, StatusSchema)
def status():
    """Retorna a saúde do serviço e do banco (503 se degradado)."""
    payload = build_status(current_app.config["TIMEZONE"])
    code = 200 if payload["status"] == "ok" else 503
    return jsonify(payload), code
