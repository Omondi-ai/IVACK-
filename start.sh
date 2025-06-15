#!/bin/bash
gunicorn university_portal.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120