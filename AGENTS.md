# AGENTS.md — instruções para agentes neste repositório

## Stack
- Python `3.15.2` (pin em `.python-version`, `requires-python = ">=3.15"` em `pyproject.toml`).
- Flask `3.1.3` com blueprints. Timezone padrão `America/Sao_Paulo` via `zoneinfo` + pacote `tzdata`.
- Gerenciador de dependências: **uv**. Nunca use `pip install` direto; use `uv sync` / `uv add` / `uv run`.
- Dev Container: `mcr.microsoft.com/devcontainers/python:3.15-trixie` + feature `uv`, `postCreateCommand` = `bash dev/dependencies.sh` (`uv sync --frozen`).

## Estrutura
- `app/__init__.py`: só `create_app()` (factory) + `db/migrate/jwt/limiter.init_app` + CORS + CLI + registro de blueprints e erros. Sem `create_all()` no runtime. `app = create_app()` existe para o Flask CLI. Prefixo de versão `/v1` aplicado centralmente (`API_PREFIX`) em todos os blueprints smorest.
- `app/config.py`: `Development/Testing/ProductionConfig` via `get_config()` (`$APP_ENV`, default development). `.env.example` documenta as vars (nunca commite `.env`; `JWT_SECRET_KEY` forte em produção).
- `app/errors.py`: handlers JSON 401/404/405/429/500 + loaders JWT no mesmo formato. `app/extensions.py`: `db`, `migrate`, `jwt`, `limiter`.
- `app/observability.py`: request-id (`X-Request-Id`), log de acesso em JSON e métricas Prometheus + `GET /metrics` (texto puro, fora do smorest de propósito).
- `app/modules/auth/`: JWT register/login/refresh/me (`User` + `UserRepository` + `TokenPairSchema`/`UserSchema`); `POST /visits` e `DELETE` exigem JWT.
- `app/modules/visits/`: exemplo com banco (CRUD + `@paginate` com header `X-Pagination` + filtro `?name=`/`?order=`); `GET/POST /visits/`, `GET/DELETE /visits/<id>`.
- `app/modules/<nome>/`: `routes.py` (bp smorest + views finas, `@paginate` quando listar), `service.py` (regra pura, sem `flask`), `schemas.py` (marshmallow: query + resposta), `models.py` + `repository.py` (**só** se o módulo tem dado — importar models no `__init__.py` para o migrate enxergar), `__init__.py` (reexporta `bp`).
- Schema do banco evolui só via `flask db migrate -m "..."` + `flask db upgrade` (`migrations/`); nunca `create_all()` no runtime (`conftest.py` é a exceção, SQLite em memória). `flask --app app seed` popula exemplo.
- `app/modules/status/`: `GET /status` com `StatusSchema`.
- `app/modules/hello_world/`: exemplo completo (`GET /`, `/hello-world`, `/hello_world`, com `?name=&lang=`, `HelloQuerySchema`/`HelloSchema`).
- Docs OpenAPI 3.1 via flask-smorest (config em `app/config.py`): `GET /openapi.json`, `/swagger-ui`, `/redoc`. Sem módulo `docs` — o spec é gerado dos blueprints.
- `tests/`: `conftest.py` (fixture `client` + `auth_headers`, `TestingConfig` + SQLite em memória), `test_routes.py`, `test_services.py` (regras puras + dublês de repository), `test_visits.py`, `test_auth.py`, `test_cli.py`.
- CI `.github/workflows/ci.yml`: ruff + pytest `--cov-fail-under=90` + pip-audit + `docker build`. Dependabot (uv/docker/actions) em `.github/dependabot.yml`.
- Pre-commit opcional local (`uvx pre-commit install`): ruff + hooks básicos (o CI é a fonte da verdade).
- `pyproject.toml` + `uv.lock`: única fonte de dependências. Não recrie `requirements.txt`.
- `dev/dependencies.sh`: apenas `uv sync --frozen`.

## Comandos
- Instalar: `uv sync` (com dev: `uv sync --group dev`).
- Rodar: `uv run flask --app app run --host 127.0.0.1 --port 40000` ou `uv run python -m flask --app app run`.
- Teste rápido de rotas: `uv run python -c "import app; c=app.app.test_client(); print(c.get('/v1/status').get_json())"`.
- Testes: `uv run --group dev pytest --cov=app --cov-report=term --cov-fail-under=90` (`conftest.py` + `test_routes/services/visits/cli/auth.py`; regra: cobrir rota nova e regra nova).
- Lint: `uv run --group dev ruff check app tests` e `ruff format --check app tests` (config em `pyproject.toml`).
- Docker (exemplo): `docker build -t base-flask .` / `docker compose up --build` (gunicorn `:40000`, `Dockerfile` + `compose.yaml`).
- Auditoria: `uv run --group dev pip-audit --desc`.
- Atualizar deps: `uv lock --upgrade` e depois `uv sync`. Commite `pyproject.toml` + `uv.lock` juntos.

## Convenções (camadas sem sobreposição)
- `routes.py`: só HTTP — lê request/`current_app.config`, chama **um** service, devolve dado puro (o `@response` serializa). Sem regra de negócio, sem dado direto.
- `service.py`: só regra de negócio, puro (sem `flask`, sem HTTP). Recebe primitivas, devolve dados.
- `repository.py`: só acesso a dado (memória/DB/arquivo/API). **Só crie quando o módulo tem fonte de dado**; sem dado, o módulo é `routes + service`.
- Respostas: devolva dado puro (dict/list/model) e deixe o `@response` serializar; `jsonify` só fora de blueprint smorest (ex. `errors.py`). Timestamps ISO 8601 com `ZoneInfo(current_app.config["TIMEZONE"])`.
- Chamadas HTTP externas (quando existirem): só `https://`, sempre com `timeout=(5, 5)` e `try/except` retornando 502/503 na rota, nunca estourar 500 sem tratamento.
- Novo módulo: criar `app/modules/<nome>/` (`routes.py` com `Blueprint` do smorest + `@arguments`/`@response` e `schemas.py`, `service.py`, `models.py` + `repository.py` se houver dado — importar models no `__init__.py`), reexportar `bp` no `__init__.py`, registrar via `api.register_blueprint` em `create_app()` com `url_prefix=f"{API_PREFIX}/<nome>"` (o `app.register_blueprint` puro não gera docs). Módulos nunca importam `app` (usar `app.extensions.db`, `current_app`).
- Proteger rota: `@jwt_required()` + `@bp.doc(security=[{"bearerAuth": []}])`. Rate limit por rota: `@limiter.limit("...")` (defaults em `RATELIMIT_DEFAULT`; Redis via `RATELIMIT_STORAGE_URI` em produção).
- Nova rota: cobrir em `tests/test_routes.py` (fixture `client`) e rodar `uv run --group dev pytest -v`.
- Não commite `.venv/`, `__pycache__/`, `*.pyc` (já no `.gitignore`).
- Debug (`FLASK_DEBUG=1`, launch.json) só local; nunca force `debug=True` no código.
