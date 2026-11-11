## O que muda?

## Por quê?

## Como testar?

- [ ] `uv run --group dev pytest --cov=app --cov-fail-under=90`
- [ ] `uv run --group dev ruff check app tests && uv run --group dev ruff format --check app tests`
- [ ] Rotas novas cobertas em `tests/` e documentadas no spec (`/openapi.json`)
- [ ] Migration criada se o schema mudou (`flask db migrate -m "..."`)
