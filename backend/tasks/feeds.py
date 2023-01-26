from celery import shared_task
from . import logger
from backend.database import crud, models
from backend.dependencies import db
import feedparser


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='feed:import')
async def import_feed(self, feed_url: str):
    logger.info("Importing URL {}", feed_url)

    sess = await db.get_db()

    if crud.get_feed_by_url(sess, feed_url) is not None:
        logger.warning("Feed already exists, not continuing")
        return None

    src = feedparser.parse(feed_url)

    if "title" in src.feed:
        db_feed = models.Feed(
            title=src.feed.title,
            url=feed_url,
            description=src.feed.description,
            owner_id=1
        )

        sess.add(db_feed)
        sess.commit()
        sess.refresh(db_feed)

    return {}
