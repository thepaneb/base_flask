# ADR 0001 — flask-smorest em vez de flask-restx para a documentação OpenAPI

Data: 2026-11-11 · Estado: aceito

## Contexto

Precisávamos expor documentação das rotas para integradores. Candidatos: `flask-restx` (sugerido inicialmente) vs `flask-smorest`.

## Decisão

`flask-smorest` (OpenAPI 3.x), testado em venv isolada no Python 3.15 + Flask 3.1.

## Por quê

- `flask-restx` 1.3.x gera só OpenAPI/Swagger **2.0** e impõe o modelo proprietário `Api/Resource`, que conflita com o padrão `routes > service > repository` do template.
- `flask-smorest` é um `Blueprint` comum (drop-in), gera OpenAPI **3.x**, valida com marshmallow e é ativamente mantido.
- Detalhe descoberto no teste: no smorest ≥0.47 os docs são opt-in (`OPENAPI_URL_PREFIX`, caminho do JSON e URLs do CDN explícitos) — configurado em `app/config.py`.

## Consequências

- Rotas usam `@bp.arguments`/`@bp.response` e `api.register_blueprint` (o `app.register_blueprint` puro não gera docs).
- `/openapi.json`, `/swagger-ui` e `/redoc` servidos pelo smorest; sem módulo `docs` próprio.
