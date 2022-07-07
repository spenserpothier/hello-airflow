from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators
from airflow.operators.bash_operator import BashOperator
from airflow.providers.discord.operators.discord_webhook import DiscordWebhookOperator
from airflow.models import Variable

with DAG(
        'mytutorial',
        default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success',
        },
        description="A simple tutorial DAG",
        schedule_interval=timedelta(minutes=2),
        start_date=datetime(2022,1,1),
        catchup=False,
        tags=['example']
) as dag:
        t1 = BashOperator(
                task_id='print_date',
                bash_command='date'
        )
        t1.doc_md = dedent(
                """\
                ### Task Documentation
                
                Added some markdown here to document this task
                """
        )

        t2 = BashOperator(
                task_id='sleep',
                depends_on_past=False,
                bash_command='sleep 1',
                retries=3
        )

        discord_webhook = Variable.get("discord_webhook")
        discord_token = Variable.get("discord_token")
        t3 = DiscordWebhookOperator(
                task_id='discord_notify',
                http_conn_id='discord',
                webhook_endpoint='webhooks/{}/{}'.format(discord_webhook, discord_token),
                message="Hello from Airflow"
        )

        dag.doc_md = dedent(
                """\
                ## Dag documentation
                
                markdown dag description
                """
        )
        t1 >> t2 >> t3
