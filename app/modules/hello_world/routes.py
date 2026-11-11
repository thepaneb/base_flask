"""Rotas do módulo hello_world (camada fina: HTTP + service + resposta).

O `Blueprint` é do flask-smorest (subclasse do Flask): valida a query,
valida/serializa a resposta e gera a documentação OpenAPI.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import current_app, jsonify
from flask_smorest import Blueprint

from .schemas import HelloQuerySchema, HelloSchema
from .service import greet

bp = Blueprint("hello_world", __name__, description="Exemplo de saudação")


@bp.route("/")
@bp.route("/hello-world")
@bp.route("/hello_world")
@bp.arguments(HelloQuerySchema, location="query")
@bp.response(200, HelloSchema)
def hello(args):
    """Saudação. Query params opcionais: `name`, `lang` (en/pt/es)."""
    message = greet(name=args.get("name"), lang=args.get("lang"))
    tz = ZoneInfo(current_app.config["TIMEZONE"])
    return jsonify({"message": message, "timestamp": datetime.now(tz).isoformat()})
