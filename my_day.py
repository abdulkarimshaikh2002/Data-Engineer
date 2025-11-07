from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from random import randint
from datetime import datetime

def training_model():
    """Simulate training and return a random accuracy (1-10)."""
    return randint(1, 10)

def _choose_best_model(ti):
    """
    Pull accuracies from XComs (returned values of the PythonOperator tasks),
    find the best one and branch to 'accurate' if best > 8, else to 'inaccurate'.
    """
    accuracies = ti.xcom_pull(
        task_ids=['training_model_A', 'training_model_B', 'training_model_C']
    )

    accuracies = [a for a in accuracies if a is not None]
    if not accuracies:
        return 'inaccurate'

    best_accuracy = max(accuracies)

    if best_accuracy > 8:
        return 'accurate'
    return 'inaccurate'

with DAG(
    dag_id='my_day',
    start_date=datetime(2025, 11, 7),
    schedule_interval='@daily',
    catchup=False,
    tags=['example']
) as dag:

    training_model_A = PythonOperator(
        task_id='training_model_A',
        python_callable=training_model
    )

    training_model_B = PythonOperator(
        task_id='training_model_B',
        python_callable=training_model
    )

    training_model_C = PythonOperator(
        task_id='training_model_C',
        python_callable=training_model
    )

    choose_best_model = BranchPythonOperator(
        task_id='choose_best_model',
        python
