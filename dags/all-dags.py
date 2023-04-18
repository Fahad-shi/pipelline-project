from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import pendulum
import os
from airflow.operators.dummy import DummyOperator
from create_tables import main_create
from insert_to_tables import main_insert
from data_to_s3 import download_data_from_source
from data_to_s3 import load_s3_data
from data_to_s3 import download_s3_data

default_args = {
    'owner': 'fahad',
    'depends_on_past': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(days=1),
    'catchup': False
}

dag = DAG(
    'Fahad_first_dag',
    default_args=default_args,
    start_date = pendulum.datetime(2023, 4, 18),
    schedule_interval = '@monthly'
)






def final_project():

    start_operator = DummyOperator(task_id='Begin_execution')

    create_tables_data_task = PythonOperator(
    task_id='create_tables',
    python_callable=main_create,
    dag=dag
    )
    
    
    download_data_from_source_task = PythonOperator(
    task_id='dowmload_source_data',
    python_callable=download_data_from_source,
    dag=dag
    )

    load_data_to_s3_task = PythonOperator(
    task_id='load_to_s3',
    python_callable=load_s3_data,
    dag=dag
    )

    download_data_from_s3_task = PythonOperator(
    task_id='download_from_s3',
    python_callable=download_s3_data,
    dag=dag
    )

    insert_data_to_tables_task = PythonOperator(
    task_id='insert_data_to_tables',
    python_callable=main_insert,
    dag=dag
    )

    end_operator = DummyOperator(task_id='end_execution')

    start_operator \
    >> create_tables_data_task \
    >> download_data_from_source_task \
    >> load_data_to_s3_task \
    >> download_data_from_s3_task \
    >> insert_data_to_tables_task \
    >> end_operator

final_project_dag = final_project()

