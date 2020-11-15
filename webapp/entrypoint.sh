#!/bin/bash

set -e

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Create superuser
echo "Create superuser"
python manage.py createsuperuser \
    --noinput \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL \
    || echo "Superuser is already created"

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
