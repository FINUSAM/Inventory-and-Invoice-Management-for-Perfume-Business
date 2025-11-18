#!/bin/bash

# Exit on error
set -o errexit

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

# Create a regular user
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user('test', 'user@example.com', 'test') if not User.objects.filter(username='test').exists() else print('User already exists')" | python manage.py shell