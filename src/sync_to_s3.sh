#!/bin/bash
set -euo pipefail

# Destination bucket
BUCKET="s3://velib-data-airflow-bucket/"

# Sync complete data/ folder to S3
aws s3 sync data "$BUCKET/data/" --delete