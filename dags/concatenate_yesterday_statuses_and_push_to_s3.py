import os
from datetime import datetime, timedelta
import platform

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from pendulum import timezone

local_tz = timezone("Europe/Paris")

default_args = {
    "owner": "Allister Kohn",
    "start_date": datetime(2025, 6, 1, tzinfo=local_tz),
    "depends_on_past": False,
    "retries": 1,
}

PYENV_PYTHON = "/home/allisterkohn/.pyenv/versions/velib_env/bin/python"
PROJECT_ROOT = os.path.dirname(__file__) + "/.."

if platform.system() == "Darwin":
    DVC_BIN = "/Users/allisterkohn/.pyenv/versions/velib-data-env/bin/dvc"
elif platform.system() == "Linux":
    DVC_BIN = "/home/allisterkohn/.pyenv/versions/velib-data-env/bin/dvc"
else:
    raise ValueError(f"Unsupported system: {platform.system()}")


with DAG(
    dag_id="concatenate_yesterday_statuses_and_push_to_s3",
    description="Pipeline to concatenate yesterday's statuses and push to S3",
    default_args=default_args,
    schedule="0 0 * * *",
    catchup=False,
    tags=[],
) as dag:

    compile_yesterday_raw_files = BashOperator(
        task_id="compile_yesterday_raw_files",
        bash_command=f"{PYENV_PYTHON} src/compile_yesterday_raw_files.py",
        cwd=str(PROJECT_ROOT),
    )

    dvc_add_and_push = BashOperator(
        task_id="dvc_add_and_push",
        bash_command=f"""
            {DVC_BIN} add data/
            {DVC_BIN} push
            {DVC_BIN} gc -c -w -f
        """,
        cwd=PROJECT_ROOT,
    )
    
    compile_yesterday_raw_files >> dvc_add_and_push