from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
import os
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

load_dotenv()
BROKER = os.getenv('BROKER')
print(BROKER)
logger = get_task_logger(__name__)

sentry_sdk.init(
    dsn=os.getenv("SENTRY_URL"),
    integrations=[
        CeleryIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    traces_sample_rate=1.0,
)

app = Celery('worker',
             broker=BROKER,
             backend='rpc://',
             include=['worker.tasks'])


if __name__ == '__main__':
    app.start()
