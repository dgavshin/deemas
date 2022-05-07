#!/usr/bin/env bash

source ./venv/bin/activate
python -m gunicorn --threads 30 --bind 0.0.0.0:5000 server:app
