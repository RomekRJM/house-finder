#!/bin/bash

HOUSE_FINDER_PATH=/home/odroid/house-finder/house-finder
HOUSE_FINDER_VENV=/home/odroid/house-finder/venv

export EMAIL_USER="your-user@test.com"
export EMAIL_PASS="emailpass"
export SMTP_SERVER="smtpserver"

source "$HOUSE_FINDER_VENV/bin/activate"
cd "$HOUSE_FINDER_PATH"
python spiders/main.py $1
deactivate
