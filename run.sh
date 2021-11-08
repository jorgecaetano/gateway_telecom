#!/bin/bash

echo Starting Gunicorn.
exec gunicorn gateway.app:app \
    --bind 0.0.0.0:8000 \
    -k gevent \
    -w 4