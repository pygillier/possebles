from kombu import Queue
from backend.settings import app_settings


def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}


class CeleryConfig:
    CELERY_BROKER_URL = app_settings.redis_dsn
    CELERY_RESULT_BACKEND = "rpc://"

    CELERY_TASK_QUEUES: list = (
        # default queue
        Queue("celery"),
        # custom queue
        Queue("feeds"),
        Queue("feed"),
    )

    CELERY_TASK_ROUTES = (route_task,)

config = CeleryConfig()
