#!/bin/sh

set -e

gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000

alembic upgrade head




