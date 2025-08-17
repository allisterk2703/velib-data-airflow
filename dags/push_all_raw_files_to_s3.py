import os
from datetime import datetime, timedelta
import platform
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Allister Kohn",
    "start_date": datetime(2025, 6, 1),
    "depends_on_past": False,
    "retries": 1,
}

if platform.system() == "Darwin":
    DVC_BIN = "/Users/allisterkohn/.pyenv/versions/velib-data-env/bin/dvc"
elif platform.system() == "Linux":
    DVC_BIN = "/home/allisterkohn/.pyenv/versions/velib-data-env/bin/dvc"
else:
    raise ValueError(f"Unsupported system: {platform.system()}")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y/%m/%d")
target_dir = f"data/station_status/raw/{yesterday}"

with DAG(
    dag_id="push_all_raw_files_to_s3",
    default_args=default_args,
    description="Pipeline to dvc add and push yesterday's raw files",
    schedule="0 0 * * *",
    catchup=False,
) as dag:

    dvc_add_and_push = BashOperator(
        task_id="dvc_add_and_push",
        bash_command=f"""
            {DVC_BIN} add "{target_dir}"
            {DVC_BIN} push
        """,
        cwd=PROJECT_ROOT,
    )

    dvc_add_and_push