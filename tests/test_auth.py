"""Testes do módulo auth (JWT: register, login, refresh, me)."""


def test_register_returns_user_without_hash(client):
    resp = client.post("/v1/auth/register", json={"username": "ada", "password": "s3cret"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["username"] == "ada"
    assert "password_hash" not in data
    assert data["id"] == 1


def test_register_duplicate_returns_409(client):
    client.post("/v1/auth/register", json={"username": "ada", "password": "s3cret"})
    resp = client.post("/v1/auth/register", json={"username": "ada", "password": "outra"})
    assert resp.status_code == 409


def test_login_returns_token_pair(client):
    client.post("/v1/auth/register", json={"username": "ada", "password": "s3cret"})
    resp = client.post("/v1/auth/login", json={"username": "ada", "password": "s3cret"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["access_token"] and data["refresh_token"]


def test_login_wrong_password_returns_401(client):
    client.post("/v1/auth/register", json={"username": "ada", "password": "s3cret"})
    resp = client.post("/v1/auth/login", json={"username": "ada", "password": "errada"})
    assert resp.status_code == 401


def test_me_requires_token(client):
    assert client.get("/v1/auth/me").status_code == 401


def test_me_with_token(auth_headers, client):
    resp = client.get("/v1/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["username"] == "ada"


def test_refresh_rotates_pair_and_rejects_old(client):
    client.post("/v1/auth/register", json={"username": "ada", "password": "s3cret"})
    tokens = client.post(
        "/v1/auth/login", json={"username": "ada", "password": "s3cret"}
    ).get_json()
    resp = client.post(
        "/v1/auth/refresh",
        headers={"Authorization": f"Bearer {tokens['refresh_token']}"},
    )
    assert resp.status_code == 200
    rotated = resp.get_json()
    assert rotated["access_token"] != tokens["access_token"]
    assert rotated["refresh_token"] != tokens["refresh_token"]

    reuse = client.post(
        "/v1/auth/refresh",
        headers={"Authorization": f"Bearer {tokens['refresh_token']}"},
    )
    assert reuse.status_code == 401


def test_logout_revokes_access_token(client, auth_headers):
    resp = client.post("/v1/auth/logout", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json() == {"message": "logged out"}

    assert client.get("/v1/auth/me", headers=auth_headers).status_code == 401


def test_logout_requires_token(client):
    assert client.post("/v1/auth/logout").status_code == 401


def test_visits_write_requires_token(client):
    assert client.post("/v1/visits/", json={"name": "Ada"}).status_code == 401
    assert client.delete("/v1/visits/1").status_code == 401


def test_visits_write_with_token(auth_headers, client):
    created = client.post("/v1/visits/", json={"name": "Ada"}, headers=auth_headers)
    assert created.status_code == 201
    visit_id = created.get_json()["id"]

    assert client.get(f"/v1/visits/{visit_id}").status_code == 200
    assert client.delete(f"/v1/visits/{visit_id}", headers=auth_headers).status_code == 204
    assert client.get(f"/v1/visits/{visit_id}").status_code == 404
