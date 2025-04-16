#!/bin/bash

alembic revision --autogenerate -m "init bd"

alembic upgrade head

gunicorn app.main:app --bind=0.0.0.0:8000