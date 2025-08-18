#!/bin/bash
set -euo pipefail

AWS_BIN="${AWS_BIN:-/usr/local/bin/aws}"
if ! command -v "$AWS_BIN" >/dev/null 2>&1; then
  echo "aws not found at $AWS_BIN" >&2
  exit 127
fi

BUCKET="s3://velib-data-airflow-bucket/"
PROJECT_DIR="/home/allisterkohn/Desktop/velib-data-airflow"

"$AWS_BIN" s3 sync "$PROJECT_DIR/data" "$BUCKET" --delete