"""Testes do módulo visits (persistência real, banco em memória)."""

import json


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


def test_get_visit_by_id_and_404(client):
    created = client.post("/visits/", json={"name": "Ada"}).get_json()

    resp = client.get(f"/visits/{created['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Ada"

    missing = client.get("/visits/999")
    assert missing.status_code == 404
    assert missing.get_json() == {"error": "not found"}


def test_delete_visit(client):
    created = client.post("/visits/", json={"name": "Ada"}).get_json()

    resp = client.delete(f"/visits/{created['id']}")
    assert resp.status_code == 204
    assert client.get(f"/visits/{created['id']}").status_code == 404

    assert client.delete("/visits/999").status_code == 404


def test_list_pagination(client):
    for i in range(3):
        client.post("/visits/", json={"name": f"n{i}"})

    page1 = client.get("/visits/?page=1&page_size=2")
    assert page1.status_code == 200
    assert len(page1.get_json()) == 2
    meta = json.loads(page1.headers["X-Pagination"])
    assert meta["total"] == 3
    assert meta["total_pages"] == 2

    page2 = client.get("/visits/?page=2&page_size=2")
    assert len(page2.get_json()) == 1
