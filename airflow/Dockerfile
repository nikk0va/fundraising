FROM apache/airflow:latest-python3.12
RUN python -m venv /home/airflow/venv \
 && /home/airflow/venv/bin/pip install --no-cache-dir \
    dbt-postgres pandas sqlalchemy "psycopg[binary]" python-dotenv requests
