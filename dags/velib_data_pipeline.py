import os
from datetime import datetime
import platform

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Allister Kohn",
    "start_date": datetime(2025, 6, 1),
    "depends_on_past": False,
    "retries": 1,
}

# Path to the virtualenv pyenv
if platform.system() == "Darwin":
    PYENV_PYTHON = "/Users/allisterkohn/.pyenv/versions/velib_env/bin/python"
elif platform.system() == "Linux":
    PYENV_PYTHON = "/home/allisterkohn/.pyenv/versions/velib_env/bin/python"
else:
    raise ValueError(f"Unsupported system: {platform.system()}")

# Root path of the project
PROJECT_ROOT = os.path.dirname(__file__) + "/.."

with DAG(
    dag_id="velib_data_pipeline",
    default_args=default_args,
    description="Pipeline to fetch and enrich Velib data",
    schedule="0,15,30,45 * * * *",  # every 15 minutes
    catchup=False,
    tags=[],
) as dag:

    fetch_velib_data = BashOperator(
        task_id="fetch_station_status",
        bash_command=f"{PYENV_PYTHON} src/fetch_velib_data.py",
        cwd=PROJECT_ROOT,
    )

    enrich_station_info_data = BashOperator(
        task_id="enrich_station_info_data",
        bash_command=f"{PYENV_PYTHON} src/enrich_velib_station_info.py",
        cwd=PROJECT_ROOT,
    )

    fetch_velib_data >> enrich_station_info_data