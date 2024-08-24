FROM postgres:16.4-alpine
LABEL authors="BRANYA43 bogdan.timchenko.2504@gmail.com"

COPY init.sh /docker-entrypoint-initdb.d/
COPY healthcheck.sh /usr/src/

RUN chmod +x /usr/src/healthcheck.sh
