#!/bin/bash

dvc add data/
dvc push
dvc gc -c -w -f