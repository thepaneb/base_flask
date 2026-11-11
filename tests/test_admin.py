"""Testes do módulo admin (requer JWT)."""


def test_stats_requires_auth(client):
    assert client.get("/v1/admin/").status_code == 401


def test_stats_returns_counts(client, auth_headers):
    client.post("/v1/visits/", json={"name": "Ada"}, headers=auth_headers)
    resp = client.get("/v1/admin/", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["users_total"] == 1
    assert data["visits_total"] == 1
    assert data["uptime_seconds"] >= 0
    assert data["version"] == "0.1.0"


def test_dashboard_renders_html(client, auth_headers):
    assert client.get("/v1/admin/dashboard").status_code == 401
    resp = client.get("/v1/admin/dashboard", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.content_type.startswith("text/html")
    body = resp.get_data(as_text=True)
    assert "Usuários" in body and "Visitas" in body
