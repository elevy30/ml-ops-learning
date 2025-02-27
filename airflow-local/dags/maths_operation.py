from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def start_number(**context):
    context['ti'].xcom_push(key='number', value=10)
    print("Start Number")

def add_five(**context):
    xcom_number = context['ti'].xcom_pull(key='number', task_ids='start_task')
    number = xcom_number + 5
    context['ti'].xcom_push(key='number', value=number)
    print(f"Add Five: {xcom_number} + 5 = {number}")

def multiply_by_two(**context):
    xcom_number = context['ti'].xcom_pull(key='number', task_ids='add_five_task')
    number = xcom_number * 2
    context['ti'].xcom_push(key='number', value=number)
    print(f"Multiply by Two: {xcom_number} * 2 = {number}")

def subtract_three(**context):
    xcom_number = context['ti'].xcom_pull(key='number', task_ids='multiply_by_two_task')
    number = xcom_number - 3
    context['ti'].xcom_push(key='number', value=number)
    print(f"Subtract Three: {xcom_number} - 3 = {number}")

def square_number(**context):
    xcom_number = context['ti'].xcom_pull(key='number', task_ids='subtract_three_task')
    number = xcom_number ** 2
    print(f"Square Number: {xcom_number} ^ 2 = {number}")

## define the DAG
with DAG(
    'maths_operation',
    description='A simple ml pipeline',
    schedule_interval='@once',
    start_date=datetime(2025, 2, 23),
    catchup=False,
    tags=["eyal"]

) as dag:

    start_task = PythonOperator(task_id='start_task', python_callable=start_number, provide_context=True)
    add_five_task = PythonOperator(task_id='add_five_task', python_callable=add_five, provide_context=True)
    multiply_by_two_task = PythonOperator(task_id='multiply_by_two_task', python_callable=multiply_by_two, provide_context=True)
    subtract_three_task = PythonOperator(task_id='subtract_three_task', python_callable=subtract_three, provide_context=True)
    square_task = PythonOperator(task_id='square_task', python_callable=square_number, provide_context=True)

    start_task >> add_five_task >> multiply_by_two_task >> subtract_three_task >> square_task