# velib-data-airflow

This project uses Apache Airflow to automatically fetch Vélib’ station status every 15 minutes, storing daily raw data under `data/station_status/raw/YYYY/MM/DD`. At midnight, a DAG adds the previous day’s folder with DVC and pushes the 96 collected files to an S3 bucket. The workflow ensures reliable scheduling, versioning, and cloud storage of Vélib’ station data.