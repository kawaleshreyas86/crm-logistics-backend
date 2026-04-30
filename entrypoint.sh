#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py migrate

echo "Creating superuser (if not exists)..."
DJANGO_SUPERUSER_USERNAME=shreyas \
DJANGO_SUPERUSER_PASSWORD=shreyas \
DJANGO_SUPERUSER_EMAIL=shreyas@example.com \
python manage.py createsuperuser --noinput || true

echo "Starting server..."
exec "$@"
