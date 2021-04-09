#!/bin/sh
source venv/bin/activate
#flask db upgrade
#flask run --host=0.0.0.0
exec gunicorn -b :5000 --access-logfile - --error-logfile - main:app