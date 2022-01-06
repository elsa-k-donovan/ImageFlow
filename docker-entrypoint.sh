#!/bin/bash

echo "Collect static files."
python DDI_Website/manage.py makemigrations

echo "Apply database migrations."
python DDI_Website/manage.py migrate

echo "Starting server."
python DDI_Website/manage.py runserver 0.0.0.0:8000

# echo "Starting celery."
# celery -A Website_Settings worker -l info