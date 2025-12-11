#!/bin/bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate