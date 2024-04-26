from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

from scraping import scraping_task
from validation import validation_task
from snowflake_load import load_data_to_snowflake
from pinecone_load import pinecone_task

with DAG("medical_data", start_date=datetime(2023, 1, 1), schedule_interval=None) as dag:

    scraping_task = PythonOperator(
        task_id="scraping_task",
        python_callable=scraping_task
    )

    validation_task = PythonOperator(
        task_id="validation_task",
        python_callable=validation_task,
        op_args=["/Users/shubh/anaconda3/lib/python3.10/site-packages/airflow/example_dags/Airflow DAG/Medline.csv"]
    )

    load_data_to_snowflake = PythonOperator(
        task_id="load_data_to_snowflake",
        python_callable=load_data_to_snowflake,
        op_args=["/Users/shubh/anaconda3/lib/python3.10/site-packages/airflow/example_dags/Airflow DAG/Medline.csv"]
    )

    pinecone_task = PythonOperator(
        task_id="pinecone_task",
        python_callable=pinecone_task
    )

    scraping_task >> validation_task >> load_data_to_snowflake >> pinecone_task