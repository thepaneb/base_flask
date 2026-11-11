"""Teste de contrato: respostas reais validadas contra o OpenAPI 3.1.

Usa o spec servido pelo app (`/openapi.json`) e valida cada corpo de
resposta com `openapi-schema-validator` (resolve `$ref` locais).
Rotas fora do contrato (doc blueprint, `/metrics`, estáticas) ficam de fora.
"""

import pytest
from openapi_schema_validator import validate


def _resolve(spec, ref):
    """Segue referências locais do tipo `#/components/...`."""
    assert ref.startswith("#/")
    node = spec
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def _dereference(node, spec):
    """Resolve recursivamente `$ref` locais (inclusive aninhados)."""
    if isinstance(node, dict):
        if set(node) == {"$ref"}:
            return _dereference(_resolve(spec, node["$ref"]), spec)
        return {k: _dereference(v, spec) for k, v in node.items()}
    if isinstance(node, list):
        return [_dereference(v, spec) for v in node]
    return node


def _response_schema(spec, path, method, status):
    op = spec["paths"][path][method]
    responses = op.get("responses", {})
    key = (
        str(status)
        if str(status) in responses
        else next((k for k in responses if k.startswith("2")), None)
    )
    assert key is not None, f"sem resposta 2xx documentada para {method.upper()} {path}"
    content = responses[key].get("content", {}).get("application/json", {})
    return _dereference(content.get("schema", {}), spec)


def _check(
    client, spec, method, path, expected_status=200, headers=None, json_body=None, spec_path=None
):
    resp = client.open(path, method=method, headers=headers, json=json_body)
    assert resp.status_code == expected_status, f"{method} {path} -> {resp.status_code}"
    if expected_status == 204:
        return resp
    clean_path = (spec_path or path).split("?")[0]
    schema = _response_schema(spec, clean_path, method.lower(), expected_status)
    validate(resp.get_json(), schema)
    return resp


@pytest.fixture()
def _user(client):
    client.post("/v1/auth/register", json={"username": "ada", "password": "s3cret"})
    tokens = client.post(
        "/v1/auth/login", json={"username": "ada", "password": "s3cret"}
    ).get_json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def test_contract_public_endpoints(client):
    spec = client.get("/openapi.json").get_json()
    _check(client, spec, "GET", "/v1/")
    _check(client, spec, "GET", "/v1/hello-world?name=Ana&lang=pt")
    _check(client, spec, "GET", "/v1/status")
    _check(client, spec, "GET", "/v1/live")


def test_contract_auth_flow(client):
    spec = client.get("/openapi.json").get_json()
    _check(
        client,
        spec,
        "POST",
        "/v1/auth/register",
        201,
        json_body={"username": "ada", "password": "s3cret"},
    )
    tokens = client.post(
        "/v1/auth/login", json={"username": "ada", "password": "s3cret"}
    ).get_json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    _check(client, spec, "GET", "/v1/auth/me", headers=headers)


def test_contract_visits_crud(client, _user):
    spec = client.get("/openapi.json").get_json()
    created = _check(
        client, spec, "POST", "/v1/visits/", 201, headers=_user, json_body={"name": "Ada"}
    ).get_json()
    _check(client, spec, "GET", "/v1/visits/?page=1&page_size=10")
    _check(
        client,
        spec,
        "GET",
        f"/v1/visits/{created['id']}",
        spec_path="/v1/visits/{visit_id}",
    )
    _check(
        client,
        spec,
        "DELETE",
        f"/v1/visits/{created['id']}",
        204,
        headers=_user,
        spec_path="/v1/visits/{visit_id}",
    )
