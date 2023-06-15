#!/bin/bash

cp -r /tmp/locale/ /src/
cp -r /tmp/translations/ /src/
python manage.py update_translations master.pot
django-admin makemessages -l en
django-admin makemessages -l es
django-admin makemessages -l fr
django-admin makemessages -l pt
python manage.py compilemessages
python manage.py migrate
python manage.py migrate_sectors # TODO: Remove when the sectors are split in production.
gunicorn tiip.wsgi:application -w 2 -b :8000 --reload --timeout 120