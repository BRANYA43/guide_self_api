FROM nginx:latest
LABEL authors="BRANYA43 bogdan.timchenko.2504@gmail.com"


RUN rm /etc/nginx/conf.d/default.conf

COPY default.conf /etc/nginx/conf.d/
COPY healthcheck.sh /usr/src/

RUN chmod +x /usr/src/healthcheck.sh
