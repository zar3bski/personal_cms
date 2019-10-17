#!/bin/sh

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "DB started"

python manage.py flush --no-input
python manage.py migrate

python manage.py loaddata ../test/data_dev.yaml 

python manage.py collectstatic --no-input --clear

exec "$@"
