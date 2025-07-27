from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dbt_dir = '/opt/airflow/dbt_project'

def build_bash_task(task_id, command):
    return BashOperator(
        task_id=task_id,
        bash_command=f"cd {dbt_dir} && {command} ",
    )

with DAG(
    'animal_nutrition_dag',
    default_args=default_args,
    description='Orchestrate DBT pipeline for animal nutrition',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['dbt', 'animal_nutrition']
) as dag:

    dbt_seed = build_bash_task('dbt_seed', 'dbt seed')
    dbt_run = build_bash_task('dbt_run', 'dbt run')
    #dbt_test = build_bash_task('dbt_test', 'dbt test --profiles-dir .')

    dbt_seed >> dbt_run