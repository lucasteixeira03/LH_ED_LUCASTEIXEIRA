# pyright: reportMissingImports=false
from datetime import datetime, timedelta
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator  # bashOperator executa comando no linux -> onde ta instalado airflow

tz = pendulum.timezone("America/Sao_Paulo")

default_args = {
    "owner": "lucas",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="banvic_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 9, 1, tzinfo=tz),
    schedule="35 4 * * *",  # agendado para 04:35 todos os dias
    catchup=False,
    max_active_runs=1,
    tags=["banvic", "etl", "iniciante"],
) as dag:

    PROJECT_DIR = "/opt/airflow/project"

    extract_postgres = BashOperator(
       task_id="extract_postgres",
       bash_command=f"cd {PROJECT_DIR} && python scripts/extracao_postgres/extracao_completa.py",
    )

    extract_transacoes = BashOperator(
       task_id="extract_transacoes",
       bash_command=f"cd {PROJECT_DIR} && python scripts/extracao_csv/extracao_transacoes.py",
    )

    load_dw = BashOperator(
       task_id="load_dw",
       bash_command=f"cd {PROJECT_DIR} && python scripts/load_dw.py",
    )

    [extract_postgres, extract_transacoes] >> load_dw
