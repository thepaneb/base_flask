# ADR 0003 — camadas routes > service > repository (+ schemas)

Data: 2026-11-11 · Estado: aceito

## Contexto

Templates Flask tendem a acumular regra de negócio nas views, o que dificulta teste e troca de persistência.

## Decisão

Todo módulo em `app/modules/<nome>/` segue:

- `routes.py`: só HTTP (lê request/config, chama **um** service, devolve dado puro; `@response` serializa).
- `service.py`: regra pura, sem `flask` e sem banco (testável sem app).
- `repository.py`: **só** se o módulo tem fonte de dado; único lugar que toca o banco.
- `schemas.py`: marshmallow (query + resposta) — alimenta validação e OpenAPI.
- `models.py`: SQLAlchemy, importado no `__init__.py` para o Alembic enxergar.

## Por quê

- Fronteiras testáveis isoladamente (unit de service com dublê de repository).
- Trocar persistência não toca rota nem regra.

## Consequências

- Módulo sem dado = `routes + service` (ex. `status`); com dado = inclui `repository` (ex. `visits`, `auth`).
- Exceções documentadas: `/metrics` (texto puro, fora do smorest) e erros JSON (`errors.py`).
