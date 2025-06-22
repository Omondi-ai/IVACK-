#!/bin/bash

echo "Waiting for database..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn university_portal.wsgi:application --bind 0.0.0.0:$PORT
