from kombu import Queue
from backend.settings import app_settings


def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}


class CeleryConfig:
    broker_url = app_settings.redis_dsn
    result_backend = "rpc://"

    worker_hijack_root_logger = False

    CELERY_TASK_QUEUES: list = (
        # default queue
        Queue("celery"),
        # custom queue
        Queue("feeds"),
        Queue("feed"),
    )

    CELERY_TASK_ROUTES = (route_task,)


config = CeleryConfig()
