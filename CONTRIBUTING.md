# Contributing (mínimo)

1. Ambiente: `uv sync --group dev` (Python 3.15 via `.python-version`).
2. Antes de abrir PR: `uv run --group dev ruff check .`, `ruff format --check .`, `pytest --cov=app --cov-fail-under=90`, `bandit -r app -q`.
3. Mudou schema? `flask db migrate -m "..."` + `upgrade` e commite a migration em `migrations/versions/`.
4. Rota nova? Cubra em `tests/`, declare schemas marshmallow (vão para o OpenAPI) e atualize a tabela de endpoints no README.
5. Sem `create_all()` no runtime, sem segredo commitado, sem `print` (use o logger em JSON).
