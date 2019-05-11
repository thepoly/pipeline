#!/bin/bash

echo Starting Gunicorn.

if [ ! -f ./.build ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
  echo "Running migrations..."
  python manage.py migrate --noinput
  date > ./.build
fi

# cd  // Change to our Django project
exec gunicorn pipeline.wsgi:application --bind 0.0.0.0:8000 --workers 3 --user pipeline --group pipeline
