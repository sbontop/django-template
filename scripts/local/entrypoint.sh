#!/bin/bash
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
