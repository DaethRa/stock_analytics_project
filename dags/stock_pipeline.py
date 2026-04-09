from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_analyst',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# 1. DAG для дневных данных
with DAG(
    'daily_stock_etl',
    default_args=default_args,
    description='Daily extraction of close prices',
    schedule_interval='0 1 * * *',
    catchup=False,
    tags=['stock_analytics'],
) as daily_dag:

    run_daily_etl = BashOperator(
        task_id='run_daily_etl',
        bash_command='cd /opt/airflow && python src/etl_daily.py'
    )

    # Убрали зависимости, теперь тут просто одна задача


# 2. DAG для реального времени
with DAG(
    'intraday_anomaly_monitor',
    default_args=default_args,
    description='Monitor prices, check anomalies, run AI, send alerts',
    schedule_interval='*/15 * * * *',
    catchup=False,
    tags=['stock_analytics'],
) as intraday_dag:

    run_intraday_etl = BashOperator(
        task_id='run_intraday_etl',
        bash_command='cd /opt/airflow && python src/etl_intraday.py'
    )

    run_ai_agent = BashOperator(
        task_id='run_ai_agent',
        bash_command='cd /opt/airflow && python src/ai_agent.py'
    )

    run_telegram_bot = BashOperator(
        task_id='run_telegram_bot',
        bash_command='cd /opt/airflow && python src/telegram_bot.py'
    )

    export_csv = BashOperator(
        task_id='export_data_for_tableau',
        bash_command='cd /opt/airflow && python src/export_to_csv.py'
    )

    # Строим цепочку напрямую с ETL
    run_intraday_etl >> run_ai_agent >> run_telegram_bot >> export_csv