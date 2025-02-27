from airflow import DAG
from airflow.decorators import task
from datetime import datetime

## define the DAG
with DAG(
    'math_seq_with_task_flow_api',
    schedule_interval='@once',
    start_date=datetime(2025, 2, 22),
    catchup=False,
    tags=["eyal"]
) as dag:

    @task
    def start_number():
        initial_value = 10
        print(f"Start Number {initial_value}")
        return initial_value

    @task
    def add_five(number):
        new_val = number + 5
        print(f"Add Five: {number} + 5 = {new_val}")
        return new_val

    @task
    def multiply_by_two(number):
        new_val = number * 2
        print(f"Multiply by Two: {number} * 2 = {new_val}")
        return new_val

    @task
    def subtract_three(number):
        new_val = number - 3
        print(f"Subtract Three: {number} - 3 = {new_val}")
        return new_val

    @task
    def square_number(number):
        new_val = number ** 2
        print(f"Square Number: {number} ^ 2 = {new_val}")
        return new_val

    start_value=start_number()
    added_value = add_five(start_value)
    multiplied_by_two = multiply_by_two(added_value)
    subtracted_three = subtract_three(multiplied_by_two)
    squared_number = square_number(subtracted_three)