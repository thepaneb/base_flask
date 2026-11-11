"""Testes das rotas da aplicação (fixture `client` em conftest.py)."""

from datetime import datetime


def test_root_returns_default_greeting(client):
    resp = client.get("/v1/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["message"] == "Hello, world!"
    datetime.fromisoformat(data["timestamp"])


def test_hello_world_aliases(client):
    for route in ("/v1/hello-world", "/v1/hello_world"):
        resp = client.get(route)
        assert resp.status_code == 200
        assert resp.get_json()["message"] == "Hello, world!"


def test_hello_with_name_and_lang(client):
    resp = client.get("/v1/hello-world?name=Ana&lang=pt")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Olá, Ana!"


def test_hello_unknown_lang_falls_back_to_default(client):
    resp = client.get("/v1/?lang=xx")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Hello, world!"


def test_status_returns_ok(client):
    resp = client.get("/v1/status")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"
    assert data["migrations"] == "ok"
    datetime.fromisoformat(data["timestamp"])


def test_live_returns_ok_without_db(client):
    resp = client.get("/v1/live")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_status_degraded_when_db_unreachable(client, monkeypatch):
    import app.modules.status.service as status_service

    monkeypatch.setattr(status_service, "check_database", lambda: False)
    resp = client.get("/v1/status")
    assert resp.status_code == 503
    data = resp.get_json()
    assert data["status"] == "degraded"
    assert data["database"] == "unreachable"


def test_status_degraded_when_migrations_pending(client, monkeypatch):
    import app.modules.status.service as status_service

    monkeypatch.setattr(status_service, "check_migrations", lambda: False)
    resp = client.get("/v1/status")
    assert resp.status_code == 503
    data = resp.get_json()
    assert data["status"] == "degraded"
    assert data["database"] == "ok"
    assert data["migrations"] == "pending"


def test_openapi_lists_registered_routes(client):
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["openapi"].startswith("3.")
    assert data["info"]["title"] == "base-flask"
    paths = set(data["paths"])
    assert {
        "/v1/status",
        "/v1/live",
        "/v1/hello-world",
        "/v1/",
        "/v1/visits/",
        "/v1/auth/register",
        "/v1/admin/",
    } <= paths


def test_openapi_spec_is_valid(client):
    from openapi_spec_validator import validate_spec

    validate_spec(client.get("/openapi.json").get_json())


def test_all_blueprint_routes_are_documented(client):
    """Contrato: toda rota (exceto /metrics, texto puro) está no spec."""
    import re

    spec_paths = client.get("/openapi.json").get_json()["paths"]
    for rule in client.application.url_map.iter_rules():
        if rule.endpoint == "static" or str(rule) == "/metrics":
            continue
        if rule.endpoint.startswith("api-docs."):
            continue  # blueprint de documentação não se auto-documenta
        # Flask <int:id> -> OpenAPI {id}
        path = re.sub(r"<(?:\w+:)?(\w+)>", r"{\1}", str(rule))
        assert path in spec_paths, f"rota fora do spec: {rule}"
        for method in rule.methods - {"HEAD", "OPTIONS"}:
            assert method.lower() in spec_paths[path], f"{method} {rule} fora do spec"


def test_metrics_exposes_prometheus_format(client):
    client.get("/v1/status")
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert resp.content_type.startswith("text/plain")
    assert "http_requests_total" in resp.get_data(as_text=True)


def test_request_id_is_echoed_and_propagated(client):
    resp = client.get("/v1/status")
    assert resp.headers["X-Request-Id"]

    sent = "abc123"
    resp2 = client.get("/v1/status", headers={"X-Request-Id": sent})
    assert resp2.headers["X-Request-Id"] == sent


def test_swagger_ui_is_served(client):
    resp = client.get("/swagger-ui")
    assert resp.status_code == 200


def test_unknown_route_returns_json_404(client):
    resp = client.get("/nao-existe")
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "not found"}


def test_method_not_allowed_returns_json_405(client):
    resp = client.post("/v1/status")
    assert resp.status_code == 405
    assert resp.get_json() == {"error": "method not allowed"}


def test_rate_limit_headers_present(client):
    resp = client.get("/v1/live")
    assert resp.status_code == 200
    assert resp.headers["X-RateLimit-Limit"] == "200"
    assert int(resp.headers["X-RateLimit-Remaining"]) >= 0


def test_rate_limit_returns_json_429():
    from app import create_app
    from app.config import TestingConfig
    from app.extensions import limiter

    app = create_app(TestingConfig)

    @app.route("/_limited")
    @limiter.limit("2 per minute")
    def limited():
        return {"ok": True}

    with app.test_client() as strict_client:
        assert strict_client.get("/_limited").status_code == 200
        assert strict_client.get("/_limited").status_code == 200
        resp = strict_client.get("/_limited")
        assert resp.status_code == 429
        assert resp.get_json() == {"error": "rate limit exceeded"}
