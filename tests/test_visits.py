"""Testes do módulo visits (persistência real, banco em memória)."""


def test_create_and_list_visits(client):
    assert client.get("/visits/").get_json() == []

    resp = client.post("/visits/", json={"name": "Ada"})
    assert resp.status_code == 201
    created = resp.get_json()
    assert created["name"] == "Ada"
    assert created["id"] == 1

    listed = client.get("/visits/").get_json()
    assert [v["name"] for v in listed] == ["Ada"]


def test_create_visit_without_name_uses_default(client):
    resp = client.post("/visits/", json={})
    assert resp.status_code == 201
    assert resp.get_json()["name"] == "anonymous"
