# ./scripts/local/entrypoint.sh


#!/bin/bash

# Wait for the database to start up
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "db" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Production
# /usr/local/bin/gunicorn ltv_forecasting_tool_backend.wsgi:application \
# --bind "0.0.0.0:$PORT" \
# --env DJANGO_SETTINGS_MODULE=ltv_forecasting_tool_backend.settings.production
# --timeout $TIMEOUT \
# --reload

# Local
/usr/local/bin/gunicorn api.wsgi:application \
--bind "0.0.0.0:$PORT" \
--env DJANGO_SETTINGS_MODULE=api.settings.local \
--timeout $TIMEOUT \
--reload
