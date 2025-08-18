#!/bin/bash

dvc add data/station_status/raw/ data/station_status/clean/ data/station_info/
dvc push
dvc gc -c -w -f