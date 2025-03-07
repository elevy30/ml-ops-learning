from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.base import BaseHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import logging
import json
from datetime import datetime


## define the DAG
with DAG(
    'nasa_apod_postgres',
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False,
    tags=["eyal"]
) as dag:

    ## step 1: Create the table if it does not exist
    @task
    def create_table():
        ## initialize the connection to the database
        ## NEED TO CREATE NEW PG CONNECTION IN AIRFLOW
        pg_hook = PostgresHook(postgres_conn_id='postgres_nasa_apod')

        create_table_sql = """
            CREATE TABLE IF NOT EXISTS nasa_apod_data (
                id Serial PRIMARY KEY,
                title VARCHAR(255),
                explanation TEXT,
                url TEXT,
                date Date,
                media_type VARCHAR(50),
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """

        ## create the table
        pg_hook.run(create_table_sql)
        return "---- Table Created ----"

    ## step 2: Extract NASA APOD data Astronomy Picture of the Day (extract pipeline)
    ## https://api.nasa.gov/planetary/apod?api_key=QEs4PSpAsBh4AgbnqudHL7qKOhnpAE06Z4lPQf0C
    @task
    def extract_apod():
        ## NEED TO CREATE NEW HTTP CONNECTION IN AIRFLOW
        conn = BaseHook.get_connection('nasa_api')
        api_key = conn.extra_dejson.get('api_key')
        logging.info(f"This is the key pulled from Airflow connection nasa_api: {api_key}")


        extract_apod_data=HttpOperator(
            task_id='extract_nasa_apod',
            http_conn_id='nasa_api', ## connection ID define In Airflow for NASA API
            endpoint='planetary/apod', ## NASA API endpoint for APOD
            method='GET',
            data={'api_key': api_key}, ## use the API key from the connection
            response_filter=lambda response:response.json()
        )
        print(extract_apod_data)
        return extract_apod_data.execute(context={})

    ## step 3: Transform the data
    @task
    def transform_apod(response):
        transformed_nasa_data = {
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),
            'media_type': response.get('media_type', '')
        }
        return transformed_nasa_data

    ## step 4: Load the data into the database
    @task
    def load_apod(transformed_nasa_data):
        pg_hook = PostgresHook(postgres_conn_id='postgres_nasa_apod')
        insert_sql = """
            INSERT INTO nasa_apod_data (title, explanation, url, date, media_type)
            VALUES (%s, %s, %s, %s, %s)
        """
        pg_hook.run(insert_sql, parameters=(
            transformed_nasa_data['title'],
            transformed_nasa_data['explanation'],
            transformed_nasa_data['url'],
            transformed_nasa_data['date'],
            transformed_nasa_data['media_type']
        ))
        return "data was loaded"

    ## step 5: Query the data from the database
    @task
    def query_apod():
        pg_hook = PostgresHook(postgres_conn_id='postgres_nasa_apod')
        records = pg_hook.get_records("SELECT * FROM nasa_apod_data")
        for record in records:
            print(record)
        return "Finish Query"


    ## step 6: Define the tasks
    create_table_task = create_table()
    apod_data = extract_apod()
    transformed_data = transform_apod(apod_data)
    load_apod_task = load_apod(transformed_data)
    query_apod_task = query_apod()

    create_table_task >> apod_data >> transformed_data >> load_apod_task >> query_apod_task
