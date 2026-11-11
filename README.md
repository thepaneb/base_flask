# base_flask

**A ready-to-use Flask workspace on VS Code Dev Containers.** Python 3.15, blueprints, dependencies managed with `uv`, debugging preconfigured, and nothing to install on your machine besides Docker.

<p>
  <a href="https://github.com/new?template_name=base_flask&template_owner=thepaneb"><img alt="Use this template" src="https://img.shields.io/badge/Use%20this%20template-2ea44f?logo=github&logoColor=white"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.15-3776AB?logo=python&logoColor=white">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white">
  <img alt="uv" src="https://img.shields.io/badge/uv-managed-5C5CFF">
  <img alt="Dev Containers" src="https://img.shields.io/badge/VS%20Code-Dev%20Containers-007ACC?logo=visualstudiocode&logoColor=white">
  <img alt="CI" src="https://github.com/thepaneb/base_flask/actions/workflows/ci.yml/badge.svg">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue">
</p>

**Landing page:** <https://thepaneb.github.io/base-flask/>

## Why use this template

- **Zero local setup** — Python and the dependencies live inside the container.
- **Python 3.15** on Debian 13 (`trixie`) with the extensions I use daily already installed (Pylance, Ruff, Black, pylint, pytest, debugpy).
- **Blueprint structure** — routes live in `app/modules/<name>/`, ready to grow without refactoring.
- **uv everywhere** — `pyproject.toml` + `uv.lock`, reproducible installs via `uv sync --frozen`.
- **Debug ready** — press `F5` and the app starts on port `40000` with breakpoints enabled.
- **Time zone set** to `America/Sao_Paulo` for reproducible dates in logs and reports.

## Quick start

1. Click **Use this template** → **Create a new repository**.
2. Clone your new repository and open the folder in VS Code.
3. Accept **Reopen in Container** when prompted (or run `Dev Containers: Reopen in Container` from the Command Palette).
4. Press **F5** and open http://127.0.0.1:40000.

Requirements: Docker running, VS Code, and the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.

To use it without creating a repository:

```sh
git clone https://github.com/thepaneb/base_flask.git
code base_flask
```

## What's inside

```text
.
├── .devcontainer/devcontainer.json   # Python 3.15-trixie image, uv feature, port 40000
├── .vscode/
│   ├── extensions.json               # recommends the Dev Containers extension
│   └── launch.json                   # "Flask Debugger" (debugpy)
├── app/
│   ├── __init__.py                   # create_app() factory, registers blueprints + errors
│   ├── config.py                     # Development/Testing/Production via APP_ENV (+ TZ, DB, JWT, CORS, rate limit, OpenAPI)
│   ├── errors.py                     # JSON 401/404/405/429/500 handlers (+ JWT loaders)
│   ├── extensions.py                 # db, migrate, jwt, limiter (init na factory)
│   ├── cli.py                        # `flask seed` (dados de exemplo, idempotente)
│   ├── logging_conf.py                 # JsonFormatter + configure_logging (nível em LOG_LEVEL)
│   ├── observability.py              # request-id, métricas Prometheus + /metrics (log via app.logger)
│   └── modules/
│       ├── hello_world/              # routes.py + service.py + repository.py + schemas.py
│       ├── status/                   # routes.py + service.py + schemas.py (GET /status + GET /live)
│       ├── visits/                   # CRUD + paginação + filtro + cache (GET/POST / + GET/DELETE /<id> + GET /export)
│       ├── auth/                     # JWT: register/login/refresh/me + User model
│       └── admin/                    # GET / (JSON stats) + GET /dashboard (HTML; requer JWT)
├── tests/                            # conftest + test_routes/services/visits/cli/auth/admin/contract/logging
├── migrations/                       # Alembic (Flask-Migrate): `flask db migrate/upgrade`
├── dev/dependencies.sh               # uv sync + flask db upgrade (container postCreate)
├── .pre-commit-config.yaml           # ruff + hooks básicos (opcional local: `uvx pre-commit install`)
├── .github/workflows/ci.yml          # ruff + pytest --cov + bandit + audit + build + smoke do container
├── .github/workflows/codeql.yml       # SAST (Python) semanal + por push/PR
├── .github/dependabot.yml            # uv + docker + github-actions (semanal)
├── Dockerfile / compose.yaml         # multi-stage, non-root, entrypoint migrate, Postgres + Redis + volumes
├── gunicorn.conf.py                  # workers/timeout/logs via env (WEB_CONCURRENCY, ...)
├── .env.example                      # APP_ENV, APP_TIMEZONE, DATABASE_URL, CORS_ORIGINS, JWT_SECRET_KEY, API_PREFIX
├── pyproject.toml / uv.lock          # Flask, smorest, SQLAlchemy, JWT, limiter, prometheus, gunicorn, tzdata
├── .python-version                   # 3.15.2
└── AGENTS.md                         # guide for coding agents
```

## Arquitetura

```mermaid
flowchart LR
    Client([Integrador]) --> Gunicorn[gunicorn :40000]
    Gunicorn --> App[create_app()]
    App --> Routes[routes.py<br/>HTTP + validação]
    Routes --> Svc[service.py<br/>regra pura]
    Svc --> Repo[repository.py<br/>SQLAlchemy]
    Repo --> DB[(Postgres / SQLite)]
    Routes -.->|cache X-Cache| Redis[(Redis)]
    App -.-> Docs[/openapi.json<br/>swagger-ui / redoc]
    Routes -.->|JWT + rate limit| Auth[JWT / limiter]
```

Camadas `routes > service > repository` sem sobreposição; `schemas.py` (marshmallow) valida entrada/saída e gera o OpenAPI; `observability.py` adiciona request-id, log JSON e métricas fora do fluxo principal.

## Endpoints (todas as rotas sob o prefixo de versão `/v1`)

| Route              | Response                                                                          |
| ------------------ | --------------------------------------------------------------------------------- |
| `GET /v1/`         | `{"message": "Hello, world!", "timestamp": ...}`                                  |
| `GET /v1/hello-world?name=Ana&lang=pt` | `{"message": "Olá, Ana!", ...}` (langs: en/pt/es, fallback en)      |
| `GET /v1/status`   | readiness: `{"status": "ok", "database": "ok", ...}` (200; 503 se degradado) |
| `GET /v1/live`     | liveness: `{"status": "ok"}` (sempre 200; para probes/healthcheck)               |
| `POST /v1/auth/register` | `{"username": "..."}` → 201 (409 se username em uso)                       |
| `POST /v1/auth/login` | `{"access_token": "...", "refresh_token": "..."}` (401 se inválido; 30 req/min) |
| `POST /v1/auth/refresh` | **rotação**: devolve par novo e revoga o refresh antigo (401 se reutilizado) |
| `POST /v1/auth/logout` | revoga o access token → 200 `{"message": "logged out"}` (requer JWT) |
| `GET /v1/auth/me`  | usuário do token (requer JWT; documentado com `security: bearerAuth`)             |
| `GET /v1/visits/`  | `[{id, name, created_at}]` paginado (`?page=&page_size=&name=&order=`, header `X-Pagination`; cache Redis/memória com header `X-Cache`) |
| `POST /v1/visits/` | `{"name": "..."}` → 201 (**requer JWT**; nome vazio vira `"anonymous"`)          |
| `GET /v1/visits/<id>` | uma visita (404 em JSON se não existir)                                       |
| `DELETE /v1/visits/<id>` | remove, 204 (**requer JWT**; 404 em JSON se não existir)                   |
| `GET /v1/visits/export` | CSV de todas as visitas (requer JWT)                                         |
| `GET /v1/admin/`   | `{"users_total", "visits_total", "uptime_seconds", "version"}` (requer JWT)      |
| `GET /openapi.json` | OpenAPI 3.1 spec (flask-smorest, com `securitySchemes` bearer)                   |
| `GET /swagger-ui`  | Swagger UI interativa (CDN; botão Authorize usa o JWT)                            |
| `GET /redoc`       | ReDoc (CDN)                                                                       |
| `GET /metrics`     | métricas Prometheus (`http_requests_total`, latência; texto puro, fora do smorest) |

Query params e respostas são validados por schemas marshmallow (`schemas.py` de cada módulo) e aparecem no spec — com `metadata={"example": ...}` para guiar integradores no Swagger UI.

## Run and debug

The container runs `bash dev/dependencies.sh` on creation, so the app is ready as soon as it opens.

| Action | How |
| --- | --- |
| Start with the debugger | `F5` → **Flask Debugger** |
| URL | http://127.0.0.1:40000 |
| Reinstall dependencies | `uv sync --group dev` (or `bash dev/dependencies.sh`) |
| Run without VS Code | `uv run flask --app app run --host 127.0.0.1 --port 40000` |

The launch profile uses `--no-debugger --no-reload` on purpose: Flask's own debugger and reloader conflict with debugpy breakpoints.

Quick check without starting a server:

```bash
uv run python -c "import app; c=app.app.test_client(); print(c.get('/v1/').get_json()); print(c.get('/v1/status').status_code)"
```

Run the test suite (`tests/`, pytest, coverage gate ≥90%):

```bash
uv run --group dev pytest --cov=app --cov-report=term --cov-fail-under=90 -v
```

`tests/conftest.py` sobe um app isolado por teste (`TestingConfig`, upgrade real das migrations em SQLite em memória); `test_services.py` cobre regras puras sem HTTP; `test_visits.py` cobre a persistência; `test_cli.py` cobre o `flask seed`; `test_contract.py` valida as respostas contra o OpenAPI.

## Database (Alembic via Flask-Migrate)

O schema evolui só por migration — nunca `create_all()` no runtime (só em testes):

```bash
uv run flask --app app db migrate -m "descreva a mudança"
uv run flask --app app db upgrade
uv run flask --app app seed   # dados de exemplo (idempotente)
```

## Observabilidade

- `request-id`: gerado por requisição (`X-Request-Id`), ecoado na resposta e incluído em todos os logs e no access log do gunicorn.
- Logs da aplicação em JSON (`app/logging_conf.py`, nível via `LOG_LEVEL`): `{"ts", "level", "logger", "request_id", ...}`.
- Métricas Prometheus em `GET /metrics` (texto puro, fora do smorest de propósito).

## Docker (exemplo)

Imagem de produção (`python:3.15-slim-trixie` + deps do `uv.lock`, usuário não-root `appuser`, gunicorn em `0.0.0.0:40000`):

```bash
docker build -t base-flask .
docker run -p 40000:40000 base-flask
# ou
docker compose up --build
```

`compose.yaml` define `APP_ENV=production`, `APP_TIMEZONE`, `DATABASE_URL=sqlite:////data/...` com volume persistente, e expõe a porta `40000`. O `entrypoint.sh` aplica `flask db upgrade` antes de subir o gunicorn. Para dev com reload, descomente o bloco `volumes`/`command` no compose. Validados: build, `compose up` (non-root), migrations no entrypoint, `GET /v1/status`, CRUD `/v1/visits` + paginação, auth JWT, `/metrics` e `/openapi.json`.

## Add a new module (`routes > service > repository`)

1. Create `app/modules/<name>/` with `routes.py` (thin: reads request/config, calls one service, returns plain data — `@response` serializes), `service.py` (pure business rule, no `flask`), `schemas.py` (marshmallow query/response), `models.py` (SQLAlchemy, if it owns tables) and `repository.py` **only if the module owns data** (re-export `bp` in `__init__.py`; import models there so migrations see them). Then `flask db migrate -m "..."` + `upgrade`.
2. Use the smorest `Blueprint` (sem `url_prefix`: o versionamento `/v1` é aplicado centralmente no `create_app`): `@bp.arguments(QuerySchema, location="query")` + `@bp.response(200, ResponseSchema)` — validation and OpenAPI come for free. Para rotas protegidas: `@jwt_required()` + `@bp.doc(security=[{"bearerAuth": []}])`; para listas: `@bp.paginate()`.
3. Register it in `create_app()` via `api.register_blueprint(<name>_bp, url_prefix=f"{prefix}/<name>")` (plain `app.register_blueprint` skips the docs).
4. Cover it in `tests/` (`test_routes.py` for HTTP incl. spec paths, `test_services.py` for pure rules; use the `client` fixture from `conftest.py`).
5. Don't import `app` inside modules (use `app.extensions.db`, `current_app.config`). Timestamps with `ZoneInfo(current_app.config["TIMEZONE"])`; external HTTP (if any) only over `https://` with `timeout=(5, 5)` and `try/except` mapped to 502/503 in the route.

## Customize

- **Dependencies:** edit `pyproject.toml`, run `uv lock && uv sync --group dev`, and commit both files.
- **Environments:** `APP_ENV=development|testing|production` (`app/config.py`); copy `.env.example` to `.env` locally (never commit `.env`). Defina um `JWT_SECRET_KEY` forte e `LOG_LEVEL` em produção.
- **Database:** `DATABASE_URL` (SQLite local por padrão, zero-setup; compose usa **Postgres** em volume persistente). Evolua só via `flask db migrate`/`upgrade` (nunca `create_all()` no runtime; `conftest.py` é a exceção, para o SQLite em memória dos testes). As migrations `create_table` são portáteis entre SQLite e Postgres.
- **Cache:** `CACHE_TYPE` (`SimpleCache` local, `RedisCache` em produção via `CACHE_REDIS_URL` — o compose já sobe o Redis com volume próprio).
- **Rate limiting:** default `200/hour` (`RATELIMIT_DEFAULT`), Redis via `RATELIMIT_STORAGE_URI` em produção com N workers; `@limiter.limit(...)` por rota (ex. login); respostas incluem headers `X-RateLimit-*`.
- **Release:** versionamento + CHANGELOG automáticos via release-please (push na `main`, conventional commits).
- **Lint local (opcional):** `uvx pre-commit install` (ruff + hooks básicos; o CI também roda pre-commit, além de ruff + pytest + audit).
- **Templates:** `CONTRIBUTING.md`, issue/PR templates em `.github/`, decisões em `docs/adr/`.
- **Port:** update `forwardPorts`/`portsAttributes` in `.devcontainer/devcontainer.json` and `--port` in `.vscode/launch.json`.
- **Security audit:** `uv run --group dev pip-audit --desc` (deps) + `uv run --group dev bandit -r app` (SAST local; CodeQL roda no CI).

Notes: `tzdata` is required on Windows for `zoneinfo`; `FLASK_DEBUG=1` (launch.json) is for local use only.

## License

MIT — see [LICENSE](LICENSE).
