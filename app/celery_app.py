import os
from celery import Celery


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery = Celery("items", broker=REDIS_URL, backend=REDIS_URL)


# Optional: small config for reliability in dev
celery.conf.update(task_ignore_result=False, result_expires=3600)