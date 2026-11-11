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
│   ├── config.py                     # Development/Testing/Production via APP_ENV (+ TZ, DB, OpenAPI)
│   ├── errors.py                     # JSON 404/405/500 handlers
│   ├── extensions.py                 # db = SQLAlchemy() (init na factory)
│   └── modules/
│       ├── hello_world/              # routes.py + service.py + repository.py + schemas.py
│       ├── status/                   # routes.py + service.py + schemas.py (GET /status, checa o DB)
│       └── visits/                   # exemplo com banco: routes + service + repository + models + schemas
├── tests/                            # conftest (app TestingConfig) + test_routes/services/visits
├── dev/dependencies.sh               # uv sync --frozen (container postCreate)
├── .github/workflows/ci.yml          # ruff + pytest + pip-audit + docker build
├── Dockerfile / compose.yaml         # exemplo prod (gunicorn :40000, volume sqlite) + .dockerignore
├── .env.example                      # APP_ENV, APP_TIMEZONE, DATABASE_URL
├── pyproject.toml / uv.lock          # dependencies (Flask, smorest, SQLAlchemy, gunicorn, tzdata)
├── .python-version                   # 3.15.2
└── AGENTS.md                         # guide for coding agents
```

## Endpoints

| Route              | Response                                                                          |
| ------------------ | --------------------------------------------------------------------------------- |
| `GET /`            | `{"message": "Hello, world!", "timestamp": ...}`                                  |
| `GET /hello-world?name=Ana&lang=pt` | `{"message": "Olá, Ana!", ...}` (langs: en/pt/es, fallback en)        |
| `GET /status`      | `{"status": "ok", "database": "ok", "timestamp": ...}` (200; 503 se degradado) |
| `GET /openapi.json` | OpenAPI 3.1 spec (flask-smorest)                                                 |
| `GET /swagger-ui`  | Swagger UI interativa (CDN)                                                       |
| `GET /redoc`       | ReDoc (CDN)                                                                       |
| `GET /visits/`     | `[{id, name, created_at}]` (SQLite via SQLAlchemy)                               |
| `POST /visits/`    | `{"name": "..."}` → 201 (nome vazio vira `"anonymous"`)                          |

Query params e respostas são validados por schemas marshmallow (`schemas.py` de cada módulo) e aparecem no spec.

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
uv run python -c "import app; c=app.app.test_client(); print(c.get('/').get_json()); print(c.get('/status').status_code)"
```

Run the test suite (`tests/`, pytest):

```bash
uv run --group dev pytest -v
```

`tests/conftest.py` sobe um app isolado por teste (`TestingConfig`, SQLite em memória); `test_services.py` cobre regras puras sem HTTP; `test_visits.py` cobre a persistência.

## Docker (exemplo)

Imagem de produção (`python:3.15-slim-trixie` + deps do `uv.lock`, servida com gunicorn em `0.0.0.0:40000`):

```bash
docker build -t base-flask .
docker run -p 40000:40000 base-flask
# ou
docker compose up --build
```

`compose.yaml` define `APP_TIMEZONE=America/Sao_Paulo` e expõe a porta `40000`. Para dev com reload, descomente o bloco `volumes`/`command` no compose. Validados: build, `compose up`, `GET /status`, `/hello-world?name=Ana&lang=pt` e `/openapi.json`.

## Add a new module (`routes > service > repository`)

1. Create `app/modules/<name>/` with `routes.py` (thin: reads request/config, calls one service, returns `jsonify`), `service.py` (pure business rule, no `flask`), `schemas.py` (marshmallow query/response), `models.py` (SQLAlchemy, if it owns tables) and `repository.py` **only if the module owns data** (re-export `bp` in `__init__.py`; import models there so `create_all()` sees them).
2. Use the smorest `Blueprint`: `@bp.arguments(QuerySchema, location="query")` + `@bp.response(200, ResponseSchema)` — validation and OpenAPI come for free.
3. Register it in `create_app()` via `api.register_blueprint(<name>_bp)` (plain `app.register_blueprint` skips the docs).
4. Cover it in `tests/` (`test_routes.py` for HTTP incl. spec paths, `test_services.py` for pure rules; use the `client` fixture from `conftest.py`).
5. Don't import `app` inside modules (use `app.extensions.db`, `current_app.config`). Timestamps with `ZoneInfo(current_app.config["TIMEZONE"])`; external HTTP (if any) only over `https://` with `timeout=(5, 5)` and `try/except` mapped to 502/503 in the route.

## Customize

- **Dependencies:** edit `pyproject.toml`, run `uv lock && uv sync --group dev`, and commit both files.
- **Environments:** `APP_ENV=development|testing|production` (`app/config.py`); copy `.env.example` to `.env` locally (never commit `.env`).
- **Database:** `DATABASE_URL` (default local SQLite file; compose maps a volume at `/data`). Schema is created via `db.create_all()` — for real projects, adopt Flask-Migrate/Alembic.
- **Port:** update `forwardPorts`/`portsAttributes` in `.devcontainer/devcontainer.json` and `--port` in `.vscode/launch.json`.
- **Security audit:** `uv run --group dev pip-audit --desc`.

Notes: `tzdata` is required on Windows for `zoneinfo`; `FLASK_DEBUG=1` (launch.json) is for local use only.

## License

MIT — see [LICENSE](LICENSE).
