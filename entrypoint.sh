#!/bin/sh
# Aplica as migrations e entrega o controle ao CMD (gunicorn).
set -e
flask --app app db upgrade
exec "$@"
