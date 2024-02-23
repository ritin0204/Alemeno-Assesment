#!/bin/bash

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Load data
python manage.py import_data

# Run the server
exec python manage.py runserver 0.0.0.0:8000
