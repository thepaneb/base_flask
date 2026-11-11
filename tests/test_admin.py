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
