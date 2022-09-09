#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Create superuser if set
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
