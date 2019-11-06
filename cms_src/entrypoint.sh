#!/bin/sh

if [ "$DATABASE" = "mariadb" ]
then
    echo "Waiting for mariadb..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "MariaDB started"
fi


python manage.py migrate

if [ "$ENV" != "prod" ]
then 
	python manage.py flush --no-input
	python manage.py loaddata ../test/fixtures/*
	pip install coverage 
fi

python manage.py collectstatic --no-input --clear


if [ "$ENV" != "prod" ]
then
	python /usr/src/cms/manage.py runserver 0.0.0.0:8000
else
	gunicorn personal_cms.wsgi:application --bind 0.0.0.0:8000
fi	

exec "$@"
