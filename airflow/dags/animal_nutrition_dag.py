from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import json
import psycopg2


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dbt_dir = '/opt/airflow/dbt_project'
ARTIFACT_PATH = "/opt/airflow/dbt_project/target/run_results.json"

def build_bash_task(task_id, command):
    return BashOperator(
        task_id=task_id,
        bash_command=f"cd {dbt_dir} && {command} ",
    )

def log_metrics_to_db():
    import json
    import psycopg2

    with open("/opt/airflow/dbt_project/target/run_results.json") as f:
        data = json.load(f)

    run_id = data['metadata']['invocation_id']
    run_started_at = data['metadata']['generated_at']

    results = data['results']

    conn = psycopg2.connect(
        dbname="animal_nutrition",
        user="dbtuser",
        password="dbtpass",
        host="postgres",
        port=5432
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dbt_run_log (
            id SERIAL PRIMARY KEY,
            run_id TEXT,
            run_started_at TIMESTAMP,
            model_id TEXT,
            status TEXT,
            execution_time FLOAT,
            materialization TEXT,
            rows_affected INTEGER,
            thread_id TEXT,
            compiled_sql TEXT,
            model_tags TEXT[],
            inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    for result in results:
        model_id = result.get('unique_id')
        status = result.get('status')
        execution_time = result.get('execution_time')
        thread_id = result.get('thread_id')
        rows_affected = result.get('adapter_response', {}).get('rows_affected', 0)
        compiled_sql = result.get('compiled_sql', '')[:1000]  # Truncate if needed

        materialization = result.get('node', {}).get('config', {}).get('materialized')
        tags = result.get('node', {}).get('tags', [])

        cursor.execute(
            """
            INSERT INTO dbt_run_log (
                run_id, run_started_at, model_id, status, execution_time,
                materialization, rows_affected, thread_id, compiled_sql, model_tags
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                run_id,
                run_started_at,
                model_id,
                status,
                execution_time,
                materialization,
                rows_affected,
                thread_id,
                compiled_sql,
                tags
            )
        )

    conn.commit()
    cursor.close()
    conn.close()



  
with DAG(
    'animal_nutrition_dag',
    default_args=default_args,
    description='Orchestrate DBT pipeline for animal nutrition',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['dbt', 'animal_nutrition']
) as dag:
    dbt_test = build_bash_task('dbt_test', 'dbt test ')
    dbt_seed = build_bash_task('dbt_seed', 'dbt seed')
    dbt_run = build_bash_task('dbt_run', 'dbt run')
    log_metrics = PythonOperator(
        task_id='log_dbt_metrics',
        python_callable=log_metrics_to_db,
        trigger_rule=TriggerRule.ALL_DONE, 
    )

    #dbt_test = build_bash_task('dbt_test', 'dbt test --profiles-dir .')

    #dbt_seed >> dbt_run >> log_metrics
    
    [dbt_seed >> dbt_run >> dbt_test ] >> log_metrics