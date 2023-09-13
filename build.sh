#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements/production.txt

python manage.py collectstatic --no-input
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User= get_user_model(); User.objects.create_superuser('abdulsalamabubakar52@gmail.com', 'abdul52.')"| python manage.py shell
