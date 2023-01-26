# Feed Service
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database import models, schemas
from backend.dependencies import db
from backend.exception import FeedException
import feedparser
import logging

logger = logging.getLogger(__name__)


class FeedService:

    def __init__(self, sess: Session = Depends(db.get_db)):
        logger.info("FeedService init")
        self._sess = sess

    def get_feeds(self, skip: int = 0, limit: int = 100) -> list[models.Feed]:
        return self._sess.query(models.Feed).offset(skip).limit(limit).all()

    def get_feed(self, feed_id: int) -> models.Feed:
        return self._sess.query(models.Feed).get(ident=feed_id)

    def get_feed_by_url(self, url: str) -> models.Feed | None:
        return self._sess.query(models.Feed).filter(models.Feed.url == url).first()

    def import_feed(self, url: str, owner: schemas.User) -> models.Feed | None:

        if self.get_feed_by_url(url=url) is not None:
            logger.warning("Feed already exists, not continuing")
            raise FeedException(code=409, message="This feed already exists!", url=url)

        src = feedparser.parse(url)

        if "title" in src.feed:
            db_feed = models.Feed(
                title=src.feed.title,
                url=url,
                description=src.feed.description,
                owner_id=owner.id
            )

            self._sess.add(db_feed)
            self._sess.commit()
            self._sess.refresh(db_feed)

            return db_feed
        else:
            raise FeedException(
                url=url,
                code=412,  # Precondition failed
                message="This URL doesn't seem to be a valid RSS/Atom feed. Please check."
            )

    def delete_feed(self, feed_id: int, owner: schemas.User):
        if self.get_feed(feed_id=feed_id) is None:
            raise FeedException(code=404, message="Unknown feed", url="")
