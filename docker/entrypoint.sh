#!/bin/sh
set -e

if [ -n "$DB_HOST_PGSGL" ]; then
  echo "Waiting for PostgreSQL at $DB_HOST_PGSGL:$DB_PORT_PGSGL..."
  while ! nc -z "$DB_HOST_PGSGL" "$DB_PORT_PGSGL"; do
    sleep 1
  done
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
