@REM ------- Initialize the Airflow environment: ---------
cd .\airflow-local\
docker compose up airflow-init


@REM ------------- Start the Airflow environment: -------------
@REM docker compose up -d

docker compose up
docker compose exec airflow-scheduler airflow db migrate
docker compose exec airflow-scheduler airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@example.com --password admin
docker compose exec airflow-webserver airflow db migrate
docker compose exec airflow-webserver airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@example.com --password admin

docker compose restart