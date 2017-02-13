#!/bin/bash

# FILL THOSE VARIABLES IN
HOUSE_FINDER_PATH=/home/odroid/house-finder/house-finder
HOUSE_FINDER_VENV=/home/odroid/house-finder/venv
ES_RUNABLE=/home/odroid/house-finder/elasticsearch-5.1.2/bin/elasticsearch

export EMAIL_USER="your-user@test.com"
export EMAIL_PASS="emailpass"
export SMTP_SERVER="smtpserver"
# END OF VARIABLE SECTION

if [ "$1" == 'start-es' ]
then
  $ES_RUNABLE &
elif [ "$1" == 'stop-es' ]
then
  ES_PROCESS="$(ps -ef | grep elasticsearch | grep java | cut -d' ' -f 5)"
  if [ ! -z "$ES_PROCESS" ]
  then
    kill -9 $ES_PROCESS
  fi
else
  source "$HOUSE_FINDER_VENV/bin/activate"
  cd "$HOUSE_FINDER_PATH"
  python spiders/main.py $1
  deactivate
fi
