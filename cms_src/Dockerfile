# pull official base image
FROM python:3.7-alpine
MAINTAINER David Zarebski <zarebskidavid@gmail.com>

# set work directory
WORKDIR /usr/src/cms

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install mysqlclient
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev mariadb-client

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pip install mysqlclient 
COPY ./Pipfile /usr/src/cms/Pipfile
RUN pipenv install --skip-lock --system --dev
RUN apk del build-deps

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/cms/entrypoint.sh

# copy project
COPY . /usr/src/cms/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/cms/entrypoint.sh"]
