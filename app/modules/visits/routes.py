"""Rotas do módulo visits (camada fina: HTTP + service + resposta)."""

from flask import abort
from flask_smorest import Blueprint

from .schemas import VisitCreateSchema, VisitSchema
from .service import delete_visit, get_visit, list_visits, record_visit

bp = Blueprint("visits", __name__, url_prefix="/visits", description="Exemplo com banco")


@bp.route("/")
@bp.response(200, VisitSchema(many=True))
@bp.paginate()
def index(pagination_parameters):
    """Lista as visitas com paginação (`?page=&page_size=`, header `X-Pagination`)."""
    items, total = list_visits(
        page=pagination_parameters.page, page_size=pagination_parameters.page_size
    )
    pagination_parameters.item_count = total
    return items


@bp.route("/", methods=["POST"])
@bp.arguments(VisitCreateSchema)
@bp.response(201, VisitSchema)
def create(args):
    """Registra uma visita. Corpo opcional: {"name": "..."}."""
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
def destroy(visit_id):
    """Remove uma visita (404 em JSON se não existir)."""
    if not delete_visit(visit_id):
        abort(404)
