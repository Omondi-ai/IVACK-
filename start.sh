#!/usr/bin/env bash
# start.sh
gunicorn university_portal.wsgi:application --workers 4 --bind 0.0.0.0:10000