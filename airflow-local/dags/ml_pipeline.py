from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

## define the task 1
def preprocess_data():
    print("Preprocess data")

## define the task 2
def train_model():
    print("Training Model")

## define the task 3
def evaluate_model():
    print("Evaluate Model")

## define the DAG
with DAG(
    'ml_pipeline',
    description='A simple ml pipeline',
    schedule_interval='@daily',
    start_date=datetime(2025, 2, 22),
    tags=["eyal"]
) as dag:

    preprocess = PythonOperator(task_id='preprocess_task', python_callable=preprocess_data)
    train = PythonOperator(task_id='train_task', python_callable=train_model)
    evaluate = PythonOperator(task_id='evaluate_task', python_callable=evaluate_model)

    preprocess >> train >> evaluate