#!/bin/sh

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
CMD python manage.py migrate --noinput && gunicorn university_portal.wsgi:application --bind 0.0.0.0:$PORT


