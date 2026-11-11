"""Rotas do módulo visits (camada fina: HTTP + service + resposta)."""

from flask import jsonify
from flask_smorest import Blueprint

from .schemas import VisitCreateSchema, VisitSchema
from .service import list_visits, record_visit

bp = Blueprint("visits", __name__, url_prefix="/visits", description="Exemplo com banco")


@bp.route("/", methods=["GET"])
@bp.response(200, VisitSchema(many=True))
def index():
    """Lista as visitas registradas."""
    return jsonify(VisitSchema(many=True).dump(list_visits()))


@bp.route("/", methods=["POST"])
@bp.arguments(VisitCreateSchema)
@bp.response(201, VisitSchema)
def create(args):
    """Registra uma visita. Corpo opcional: {"name": "..."}."""
    visit = record_visit(args.get("name"))
    return jsonify(VisitSchema().dump(visit)), 201
