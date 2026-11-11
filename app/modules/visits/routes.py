"""Rotas do módulo visits (camada fina: HTTP + service + resposta)."""

from flask import abort
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from .schemas import VisitCreateSchema, VisitListQuerySchema, VisitSchema
from .service import delete_visit, get_visit, list_visits, record_visit

bp = Blueprint("visits", __name__, description="Exemplo com banco")

_bearer = [{"bearerAuth": []}]


@bp.route("/")
@bp.response(200, VisitSchema(many=True))
@bp.paginate()
@bp.arguments(VisitListQuerySchema, location="query")
def index(filter_args, pagination_parameters):
    """Lista as visitas com filtro (`?name=`), ordem (`?order=asc|desc`) e paginação."""
    items, total = list_visits(
        page=pagination_parameters.page,
        page_size=pagination_parameters.page_size,
        name=filter_args.get("name"),
        order=filter_args.get("order") or "desc",
    )
    pagination_parameters.item_count = total
    return items


@bp.route("/", methods=["POST"])
@bp.arguments(VisitCreateSchema)
@bp.response(201, VisitSchema)
@jwt_required()
@bp.doc(security=_bearer)
def create(args):
    """Registra uma visita (requer JWT). Corpo opcional: {"name": "..."}."""
    return record_visit(args.get("name"))


@bp.route("/<int:visit_id>")
@bp.response(200, VisitSchema)
def show(visit_id):
    """Retorna uma visita pelo id (404 em JSON se não existir)."""
    visit = get_visit(visit_id)
    if visit is None:
        abort(404)
    return visit


@bp.route("/<int:visit_id>", methods=["DELETE"])
@bp.response(204)
@jwt_required()
@bp.doc(security=_bearer)
def destroy(visit_id):
    """Remove uma visita (requer JWT; 404 em JSON se não existir)."""
    if not delete_visit(visit_id):
        abort(404)
