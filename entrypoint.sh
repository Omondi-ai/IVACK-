#!/bin/sh

set -e

# Wait for database to be ready (only needed if using Docker Compose)
if [ "$DB_HOST" ]; then
  until nc -z -v -w30 "$DB_HOST" 5432; do
    echo "Waiting for database connection..."
    sleep 5
  done
fi

# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8000 university_portal.wsgi