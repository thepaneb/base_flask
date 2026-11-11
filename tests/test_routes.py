"""Testes das rotas da aplicação (fixture `client` em conftest.py)."""

from datetime import datetime


def test_root_returns_default_greeting(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["message"] == "Hello, world!"
    datetime.fromisoformat(data["timestamp"])


def test_hello_world_aliases(client):
    for route in ("/hello-world", "/hello_world"):
        resp = client.get(route)
        assert resp.status_code == 200
        assert resp.get_json()["message"] == "Hello, world!"


def test_hello_with_name_and_lang(client):
    resp = client.get("/hello-world?name=Ana&lang=pt")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Olá, Ana!"


def test_hello_unknown_lang_falls_back_to_default(client):
    resp = client.get("/?lang=xx")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Hello, world!"


def test_status_returns_ok(client):
    resp = client.get("/status")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"
    datetime.fromisoformat(data["timestamp"])


def test_status_degraded_when_db_unreachable(client, monkeypatch):
    import app.modules.status.service as status_service

    monkeypatch.setattr(status_service, "check_database", lambda: False)
    resp = client.get("/status")
    assert resp.status_code == 503
    data = resp.get_json()
    assert data["status"] == "degraded"
    assert data["database"] == "unreachable"


def test_openapi_lists_registered_routes(client):
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["openapi"].startswith("3.")
    assert data["info"]["title"] == "base-flask"
    paths = set(data["paths"])
    assert {"/status", "/hello-world", "/", "/visits/"} <= paths


def test_swagger_ui_is_served(client):
    resp = client.get("/swagger-ui")
    assert resp.status_code == 200


def test_unknown_route_returns_json_404(client):
    resp = client.get("/nao-existe")
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "not found"}


def test_method_not_allowed_returns_json_405(client):
    resp = client.post("/status")
    assert resp.status_code == 405
    assert resp.get_json() == {"error": "method not allowed"}
