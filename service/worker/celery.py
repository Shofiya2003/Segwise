from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
import os

# import sentry_sdk
# from sentry_sdk.integrations.celery import CeleryIntegration

load_dotenv()
BROKER = os.getenv('BROKER')
print(BROKER)
logger = get_task_logger(__name__)

# sentry_sdk.init(
#     dsn='https://372937d59fce20a4907626350c7bfa91@o4505625999966208.ingest.sentry.io/4505626005995520',
#     integrations=[
#         CeleryIntegration(),
#     ],

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production,
#     traces_sample_rate=1.0,
# )

app = Celery('worker',
             broker=BROKER,
             backend='rpc://',
             include=['worker.tasks'])


if __name__ == '__main__':
    app.start()
