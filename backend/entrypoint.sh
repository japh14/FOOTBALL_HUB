#!/bin/bash
set -e

echo ">>> Running database migrations..."
python manage.py migrate --noinput

echo ">>> Collecting static files..."
python manage.py collectstatic --noinput

echo ">>> Ensuring media directory exists..."
mkdir -p /app/media

echo ">>> Executing command: $@"
# Replace shell with the command (proper signal handling)
exec "$@"