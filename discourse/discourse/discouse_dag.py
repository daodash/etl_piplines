from airflow import DAG
from airflow.operators.python import PythonOperator
from main import pull_categories, pull_users, pull_topics, pull_posts_and_polls

with DAG(
    dag_id='discourse_dag',
    description='DAODash Discourse DAG',
    schedule_interval=None,
    catchup=False,
    tags=None,
) as dag:

    pull_categories_task = PythonOperator(
        task_id='pull_categories',
        python_callable=pull_categories,
    )

    pull_users_task = PythonOperator(
        task_id='pull_users',
        python_callable=pull_users,
    )

    pull_topics_task = PythonOperator(
        task_id='pull_topics',
        python_callable=pull_topics,
    )

    pull_posts_and_polls_task = PythonOperator(
        task_id='pull_posts_and_polls',
        python_callable=pull_posts_and_polls,
    )

    [pull_categories_task, pull_users_task] >> pull_topics_task >> pull_posts_and_polls_task
