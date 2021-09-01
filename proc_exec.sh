#!/bin/bash

set -x

eval $(printenv | awk -F= '{print "export " "\""$1"\"""=""\""$2"\"" }' >> /etc/profile)
printenv | awk -F= '{print "export " "\""$1"\"""=""\""$2"\"" }'

echo "pass through variables: "
echo $ENV_BUILD
echo $PROJECT_NAME
echo $REDIS_URL

echo 'Starting Processes'

#python -m pip install psutil
#python -m pip install asyncpg
#python -m pip install apscheduler

#if [ $PROJECT_NAME = "pricing-api" ]; then
#
#  if [ $ENV_BUILD = "loc" ]; then
#    echo '-------------------------------'
#    echo 'Requirement to run on local:'
#    echo '1. redis-server'
#    echo '2. rq-dashboard'
#    echo '3. chmod(optional)'
#    echo '4. jupyter-lab'
#    echo '-------------------------------'
#
#    echo "Spinning up redis-server for local environment"
#    # For Local Testing, Start the first redis server process
#    redis-server --protected-mode no --port 6379 &
#    REDISS=$!
#    status=$?
#    if [ $status -ne 0 ]; then
#      echo "Failed to start redis server process: $status"
#      exit $status
#    fi
#
#  else   #dev & prod
#    echo '-------------------------------'
#    echo 'Requirement to run on dev/prod:'
#    echo '1. rq-dashboard'
#    echo '2. chmod'
#    echo '3. jupyter-lab'
#    echo '-------------------------------'
#  fi
#
#  rq-dashboard -u $REDIS_URL --port 9181 & RQDASH=$!
#  status=$?
#  if [ $status -ne 0 ]; then
#    echo "Failed to start rq dashboard: $status"
#    exit $status
#  fi
#
#  echo 'Starting cron'
##  cp cron/cron_jobs /etc/cron.d/cron_jobs
#  chmod 0644 /etc/cron.d/cron_jobs
#  crontab /etc/cron.d/cron_jobs
#  /etc/init.d/cron start & CRONEX=$!
#  status=$?
#  if [ $status -ne 0 ]; then
#      echo "Failed to start cron process: $status"
#    exit $status
#  fi
#
#  # Start the second jupyter-lab process
#  jupyter lab --ip='0.0.0.0' --port=8888 --no-browser --allow-root & JPTRLB=$!
#  status=$?
#  if [ $status -ne 0 ]; then
#    echo "Failed to start jupyter lab process: $status"
#    exit $status
#  fi
#
#  ## Start the first gunicorn process to invoke leader
#  gunicorn -w 1 -b 0.0.0.0:5000 app:app --reload & GUNICO=$!
#  status=$?
#  if [ $status -ne 0 ]; then
#    echo "Failed to start gunicorn process: $status"
#    exit $status
#  fi
#
#  wait $RQDASH
#  wait $JPTRLB
#  wait $GUNICO
#
#fi

echo 'RUNNING FIRST IF:'
echo 'Project Name:'
echo $PROJECT_NAME

if [ $PROJECT_NAME = "pricing-api" ]; then

  if [ $ENV_BUILD = "loc" ]; then
    echo '-------------------------------'
    echo 'Requirement to run on local:'
    echo '1. redis-server'
    echo '2. worker.py'
    echo '3. gunicorn'
    echo '4. jupyter-lab'
    echo '-------------------------------'
    echo "Spinning up redis-server for local environment"

    # For Local Testing, Start the first redis server process
    redis-server --protected-mode no --port 6379 &
    REDISS=$!
    status=$?
    if [ $status -ne 0 ]; then
      echo "Failed to start redis server process: $status"
      exit $status
    fi

  else   #dev & prod
    echo '-------------------------------'
    echo 'Requirement to run on dev/prod:'
    echo '1. rq-dashboard'
    echo '2. chmod'
    echo '3. jupyter-lab'
    echo '-------------------------------'
  fi

#  rq-dashboard -u $REDIS_URL --port 9181 & RQDASH=$!
#  status=$?
#  if [ $status -ne 0 ]; then
#    echo "Failed to start rq dashboard: $status"
#    exit $status
#  fi

  # Start the rq worker process
  python worker.py & WORKER=$!
  status=$?
  if [ $status -ne 0 ]; then
    echo "Failed to start worker process: $status"
    exit $status
  fi

  # Start the first gunicorn process
  gunicorn -w 2 -b 0.0.0.0:5000 app:app --reload & GUNICO=$!
  status=$?
  if [ $status -ne 0 ]; then
    echo "Failed to start gunicorn process: $status"
    exit $status
  fi

  # Start the second jupyter-lab process
  jupyter lab --ip='0.0.0.0' --port=8888 --no-browser --allow-root & JPTRLB=$!
  status=$?
  if [ $status -ne 0 ]; then
    echo "Failed to start jupyter lab process: $status"
    exit $status
  fi

#  wait $RQDASH
  wait $WORKER
  wait $GUNICO
  wait $JPTRLB

fi

#fi

#  else
#    echo '-------------------------------'
#    echo 'Requirement to run on dev/prod:'
#    echo '2. worker.py'
#    echo '3. gunicorn'
#    echo '-------------------------------'
#
#    # Start the rq worker process
#    python worker.py & WORKER1=$!
#    status=$?
#    if [ $status -ne 0 ]; then
#      echo "Failed to start gunicorn process: $status"
#      exit $status
#    fi
#
#    python worker.py & WORKER2=$!
#    status=$?
#    if [ $status -ne 0 ]; then
#      echo "Failed to start gunicorn process: $status"
#      exit $status
#    fi
#
#    ## Start the first gunicorn process
#    gunicorn -w 2 -b 0.0.0.0:5000 app:app --reload & GUNICO=$!
#    status=$?
#    if [ $status -ne 0 ]; then
#      echo "Failed to start gunicorn process: $status"
#      exit $status
#    fi
#
##    jupyter lab --ip='0.0.0.0' --port=8888 --no-browser --allow-root & JPTRLB=$!
##    status=$?
##    if [ $status -ne 0 ]; then
##      echo "Failed to start jupyter lab process: $status"
##      exit $status
##    fi
#
#    wait $WORKER1
#    wait $WORKER2
#    wait $GUNICO
##    wait $JPTRLB
#
#  fi
#fi
