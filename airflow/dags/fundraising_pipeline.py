from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

PY = "/home/airflow/venv/bin/python"
DBT = "/home/airflow/venv/bin/dbt"
ING = "cd /opt/project/ingest &&"

with DAG(
    dag_id="fundraising_pipeline",
    start_date=datetime(2026, 10, 1),
    schedule="*/5 * * * *",
    catchup=False,
    max_active_runs=1,
) as dag:
    load_campaigns = BashOperator(task_id="load_campaigns",
        bash_command=f"{ING} {PY} load_campaigns.py")
    fetch_api = BashOperator(task_id="fetch_api",
        bash_command=f"{ING} {PY} fetch_api.py 99")
    dbt_build = BashOperator(task_id="dbt_build",
        bash_command=f"{DBT} build --project-dir /opt/project/dbt")

    load_campaigns >> fetch_api >> dbt_build
