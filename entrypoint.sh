#!/bin/sh
set -e

# Apply database migrations against the configured (Postgres) database, then
# hand off to the container's main process (gunicorn by default).
python manage.py migrate --noinput

exec "$@"
