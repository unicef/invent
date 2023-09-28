#!/bin/bash

cp -r /tmp/locale/ /src/
cp -r /tmp/translations/ /src/
python manage.py update_translations master.pot
django-admin makemessages -l en
django-admin makemessages -l es
django-admin makemessages -l fr
django-admin makemessages -l pt
python manage.py collectstatic --noinput
python manage.py compilemessages
python manage.py migrate --fake project 0113_alter_historicalprojectapproval_options_and_more || echo "Could not fake the migration, continuing anyway."
python manage.py migrate
gunicorn tiip.wsgi:application -w 2 -b :8000 --reload --timeout 120