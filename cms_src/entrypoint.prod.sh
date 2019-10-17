#!/bin/sh

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "DB started"

python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"
