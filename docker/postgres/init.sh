#!/bin/bash

# finish script if some error is raised
set -e

# create a user and give the user all privileges
psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "${POSTGRES_DB}" <<-EOSQL
  ALTER ROLE ${POSTGRES_USER} SET client_encoding TO 'utf-8';
  ALTER ROLE ${POSTGRES_USER} SET timezone TO 'UTC';
  GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};
EOSQL
