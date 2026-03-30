from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import TaskGroup

from airflow.providers.standard.operators.python import PythonOperator
import time


def print_hello():
    print("Hello from Python!")

def slow():
    time.sleep(2)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    dag_id="example_complex_dag_v3",
    description="Complex DAG with task groups and parallelism (Airflow 3)",
    default_args=default_args,
    schedule=None,  # manual only
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["example", "taskgroup", "airflow3"],
) as dag:



    start = PythonOperator(
        task_id="start_process",
        python_callable=slow,
    )
    python_init = PythonOperator(
        task_id="python_init",
        python_callable=print_hello,
    )

    with TaskGroup(
        group_id="data_preparation_group",
        tooltip="Data preparation steps",
    ) as data_prep:

        download = BashOperator(
            task_id="download_data",
            bash_command='echo "downloading"',
        )

        check = BashOperator(
            task_id="check_file",
            bash_command='echo "checking"',
        )

        unzip = BashOperator(
            task_id="unzip_file",
            bash_command='echo "unzipping"',
        )

        with TaskGroup(
            group_id="validation_subsection",
            tooltip="Validation steps",
        ) as validation:

            validate_schema = BashOperator(
                task_id="validate_schema",
                bash_command='echo "schema ok"',
            )

            validate_counts = BashOperator(
                task_id="validate_counts",
                bash_command='echo "counts ok"',
            )

            validate_schema >> validate_counts

        download >> check >> unzip >> validation

    with TaskGroup(
        group_id="processing_group",
        tooltip="Main processing",
    ) as processing:

        proc_init = BashOperator(
            task_id="proc_init",
            bash_command="sleep 1",
        )

        shards = [
            BashOperator(task_id=f"proc_shard_{i}", bash_command=f"echo {i}")
            for i in range(1, 6)
        ]

        reduce_step = BashOperator(
            task_id="proc_reduce",
            bash_command="echo reduce",
        )

        finalize = BashOperator(
            task_id="proc_finalize",
            bash_command="echo done",
        )

        proc_init >> shards >> reduce_step >> finalize

    with TaskGroup(
        group_id="reporting_group",
        tooltip="Reporting and delivery",
    ) as reporting:

        pdf = BashOperator(
            task_id="gen_report_pdf",
            bash_command="echo pdf",
        )

        csv = BashOperator(
            task_id="gen_report_csv",
            bash_command="echo csv",
        )

        send = BashOperator(
            task_id="send_email",
            bash_command="echo email",
        )

        archive = BashOperator(
            task_id="archive_report",
            bash_command="echo archive",
        )

        [pdf, csv] >> send >> archive

    end = BashOperator(
        task_id="end_process",
        bash_command='echo "Process finished"',
    )

    start >> python_init >> data_prep >> processing >> reporting >> end