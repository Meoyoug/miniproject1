#!/bin/sh

set -e


# python wait_for_db.py

gunicron -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8000

alembic upgrade head




