"""Rotas do módulo visits (camada fina: HTTP + service + resposta)."""

import csv
import io
from datetime import datetime
from types import SimpleNamespace

from flask import Response, abort, current_app
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.extensions import cache

from .schemas import VisitCreateSchema, VisitListQuerySchema, VisitSchema
from .service import delete_visit, export_visits, get_visit, list_visits, record_visit

bp = Blueprint("visits", __name__, description="Exemplo com banco")

_bearer = [{"bearerAuth": []}]
LIST_VERSION_KEY = "visits:list:version"


def _bump_list_version():
    """Invalida o cache da listagem (namespace por versão)."""
    cache.set(LIST_VERSION_KEY, (cache.get(LIST_VERSION_KEY) or 0) + 1)


@bp.route("/")
@bp.response(200, VisitSchema(many=True))
@bp.paginate()
@bp.arguments(VisitListQuerySchema, location="query")
def index(filter_args, pagination_parameters):
    """Lista as visitas com filtro, ordem e paginação (com cache + header `X-Cache`)."""
    version = cache.get(LIST_VERSION_KEY) or 0
    key = (
        f"visits:list:v{version}:p{pagination_parameters.page}"
        f":s{pagination_parameters.page_size}:n{filter_args.get('name') or ''}"
        f":o{filter_args.get('order') or 'desc'}"
    )
    hit = cache.get(key)
    if hit is not None:
        # O cache guarda dicts (JSON-safe); reidrata para o @response serializar.
        items = [
            SimpleNamespace(
                id=i["id"],
                name=i["name"],
                created_at=datetime.fromisoformat(i["created_at"]),
            )
            for i in hit["items"]
        ]
        pagination_parameters.item_count = hit["total"]
        return items, 200, {"X-Cache": "HIT"}

    items, total = list_visits(
        page=pagination_parameters.page,
        page_size=pagination_parameters.page_size,
        name=filter_args.get("name"),
        order=filter_args.get("order") or "desc",
    )
    pagination_parameters.item_count = total
    payload = VisitSchema(many=True).dump(items)
    cache.set(
        key, {"items": payload, "total": total}, timeout=current_app.config["CACHE_LIST_TIMEOUT"]
    )
    return items, 200, {"X-Cache": "MISS"}


@bp.route("/", methods=["POST"])
@bp.arguments(VisitCreateSchema)
@bp.response(201, VisitSchema)
@jwt_required()
@bp.doc(security=_bearer)
def create(args):
    """Registra uma visita (requer JWT). Corpo opcional: {"name": "..."}."""
    visit = record_visit(args.get("name"))
    _bump_list_version()
    return visit


@bp.route("/<int:visit_id>")
@bp.response(200, VisitSchema)
def show(visit_id):
    """Retorna uma visita pelo id (404 em JSON se não existir; com cache)."""
    key = f"visits:item:{visit_id}"
    hit = cache.get(key)
    if hit is not None:
        item = SimpleNamespace(
            id=hit["id"],
            name=hit["name"],
            created_at=datetime.fromisoformat(hit["created_at"]),
        )
        return item, 200, {"X-Cache": "HIT"}
    visit = get_visit(visit_id)
    if visit is None:
        abort(404)
    cache.set(key, VisitSchema().dump(visit), timeout=current_app.config["CACHE_DETAIL_TIMEOUT"])
    return visit, 200, {"X-Cache": "MISS"}


@bp.route("/<int:visit_id>", methods=["DELETE"])
@bp.response(204)
@jwt_required()
@bp.doc(security=_bearer)
def destroy(visit_id):
    """Remove uma visita (requer JWT; 404 em JSON se não existir)."""
    if not delete_visit(visit_id):
        abort(404)
    cache.delete(f"visits:item:{visit_id}")
    _bump_list_version()


@bp.get("/export")
@jwt_required()
@bp.doc(security=_bearer)
def export():
    """Exporta todas as visitas em CSV (requer JWT; texto puro, fora do @response)."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "created_at"])
    for visit in export_visits():
        writer.writerow([visit.id, visit.name, visit.created_at.isoformat()])
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=visits.csv"},
    )
