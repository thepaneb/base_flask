"""Testes do módulo visits (persistência real, banco em memória)."""

import json


def test_create_and_list_visits(client, auth_headers):
    assert client.get("/v1/visits/").get_json() == []

    resp = client.post("/v1/visits/", json={"name": "Ada"}, headers=auth_headers)
    assert resp.status_code == 201
    created = resp.get_json()
    assert created["name"] == "Ada"
    assert created["id"] == 1

    listed = client.get("/v1/visits/").get_json()
    assert [v["name"] for v in listed] == ["Ada"]


def test_create_visit_without_name_uses_default(client, auth_headers):
    resp = client.post("/v1/visits/", json={}, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.get_json()["name"] == "anonymous"


def test_get_visit_by_id_and_404(client, auth_headers):
    created = client.post("/v1/visits/", json={"name": "Ada"}, headers=auth_headers).get_json()

    resp = client.get(f"/v1/visits/{created['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Ada"

    missing = client.get("/v1/visits/999")
    assert missing.status_code == 404
    assert missing.get_json() == {"error": "not found"}


def test_delete_visit(client, auth_headers):
    created = client.post("/v1/visits/", json={"name": "Ada"}, headers=auth_headers).get_json()

    resp = client.delete(f"/v1/visits/{created['id']}", headers=auth_headers)
    assert resp.status_code == 204
    assert client.get(f"/v1/visits/{created['id']}").status_code == 404

    assert client.delete("/v1/visits/999", headers=auth_headers).status_code == 404


def test_list_pagination(client, auth_headers):
    for i in range(3):
        client.post("/v1/visits/", json={"name": f"n{i}"}, headers=auth_headers)

    page1 = client.get("/v1/visits/?page=1&page_size=2")
    assert page1.status_code == 200
    assert len(page1.get_json()) == 2
    meta = json.loads(page1.headers["X-Pagination"])
    assert meta["total"] == 3
    assert meta["total_pages"] == 2

    page2 = client.get("/v1/visits/?page=2&page_size=2")
    assert len(page2.get_json()) == 1


def test_list_filter_and_order(client, auth_headers):
    client.post("/v1/visits/", json={"name": "Ada"}, headers=auth_headers)
    client.post("/v1/visits/", json={"name": "Grace"}, headers=auth_headers)

    filtered = client.get("/v1/visits/?name=ada").get_json()
    assert [v["name"] for v in filtered] == ["Ada"]

    asc = client.get("/v1/visits/?order=asc").get_json()
    assert [v["name"] for v in asc] == ["Ada", "Grace"]

    invalid = client.get("/v1/visits/?order=sideways")
    assert invalid.status_code == 422


def test_list_cache_headers_and_invalidation(client, auth_headers):
    first = client.get("/v1/visits/")
    assert first.headers["X-Cache"] == "MISS"

    second = client.get("/v1/visits/")
    assert second.headers["X-Cache"] == "HIT"
    assert second.get_json() == first.get_json()

    client.post("/v1/visits/", json={"name": "Ada"}, headers=auth_headers)
    third = client.get("/v1/visits/")
    assert third.headers["X-Cache"] == "MISS"
    assert [v["name"] for v in third.get_json()] == ["Ada"]


def test_export_csv_requires_auth(client):
    assert client.get("/v1/visits/export").status_code == 401


def test_export_csv(client, auth_headers):
    client.post("/v1/visits/", json={"name": "Ada"}, headers=auth_headers)
    resp = client.get("/v1/visits/export", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.content_type.startswith("text/csv")
    body = resp.get_data(as_text=True)
    assert body.splitlines()[0] == "id,name,created_at"
    assert ",Ada," in body
