#!/bin/sh

python3 manage.py migrate

/usr/local/bin/gunicorn contact_processor.wsgi -w 4 -b 0.0.0.0:8000 -t 0 --reload

exec "$@"
