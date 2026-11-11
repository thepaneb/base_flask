# ADR 0002 — uv como único gerenciador de dependências

Data: 2026-11-11 · Estado: aceito

## Contexto

O projeto nasceu com `pip install -r app/requirements.txt` e upgrade global de pacotes no `dev/dependencies.sh` (não reproduzível).

## Decisão

`pyproject.toml` + `uv.lock` como única fonte; `uv sync --frozen` no devcontainer/CI; sem `requirements.txt`; sem `pip install` direto (ver `AGENTS.md`).

## Por quê

- Lock travado + sync reproduzível em dev, CI e Docker (multi-stage copia só o `.venv`).
- `uv` já vem como feature do devcontainer; `pip-audit`, `ruff` e `bandit` rodam via `uv run`.

## Consequências

- Atualizar deps = `uv lock --upgrade && uv sync` (commite os dois arquivos).
- `pip-audit --locked` não é necessário: o lock é a fonte auditada.
