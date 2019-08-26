FROM nginx:1.15.12-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# install certbot
RUN apk update \
    && apk add certbot