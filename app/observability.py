"""Observabilidade: request-id, log de acesso em JSON e métricas Prometheus.

Um único `init_observability(app)` registra os hooks; o blueprint expõe
o `/metrics` em texto puro (fora do smorest de propósito). O log de
acesso usa `app.logger`, já formatado em JSON por `logging_conf`.
"""

import time
import uuid

from flask import Blueprint, Response, current_app, g, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

bp = Blueprint("metrics", __name__)

REQUESTS = Counter(
    "http_requests_total",
    "Total de requisições HTTP.",
    ["method", "endpoint", "status"],
)
DURATION = Histogram(
    "http_request_duration_seconds",
    "Duração das requisições HTTP.",
    ["method", "endpoint"],
)


def init_observability(app):
    """Registra request-id, log JSON e métricas (ignora o próprio /metrics)."""

    @app.before_request
    def _start_request():
        g.request_id = request.headers.get("X-Request-Id") or uuid.uuid4().hex
        g._started_at = time.perf_counter()

    @app.after_request
    def _finish_request(response):
        response.headers["X-Request-Id"] = g.get("request_id", "-")
        if request.path == "/metrics":
            return response
        elapsed_ms = (time.perf_counter() - g.get("_started_at", time.perf_counter())) * 1000
        endpoint = request.endpoint or "unknown"
        REQUESTS.labels(request.method, endpoint, response.status_code).inc()
        DURATION.labels(request.method, endpoint).observe(elapsed_ms / 1000)
        current_app.logger.info(
            {
                "method": request.method,
                "path": request.path,
                "endpoint": endpoint,
                "status": response.status_code,
                "duration_ms": round(elapsed_ms, 2),
            }
        )
        return response


@bp.get("/metrics")
def metrics():
    """Expõe as métricas no formato do Prometheus."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
