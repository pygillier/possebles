from celery import shared_task
from . import logger


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='feed:import')
async def import_feed(self, feed_url: str):
    pass
