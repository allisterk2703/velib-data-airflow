#!/bin/bash

export AIRFLOW_HOME=$HOME/Desktop/velib-data-airflow/airflow
export PATH=$HOME/.pyenv/versions/velib-data-env/bin:/usr/bin:/bin

# Start the scheduler in the background
airflow scheduler &

# Start the webserver in the foreground with port 8100
exec airflow webserver --port 8100