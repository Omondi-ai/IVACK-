#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
/app/wait-for-postgres.sh "$DB_HOST"

echo "PostgreSQL started"

# Ensure staticfiles directory exists and is owned by appuser
mkdir -p /app/staticfiles
chown -R appuser:appuser /app/staticfiles

# Run Django management commands
python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput

exec gunicorn university_portal.wsgi:application --bind 0.0.0.0:8000
