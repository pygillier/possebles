# Feed Service
import datetime
from time import mktime
import pytz

from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database import models, schemas
from backend.dependencies import db
from backend.exception import FeedException
from .mastodon import MastodonService
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

    def delete_feed(self, feed_id: int, owner: schemas.User) -> bool:
        feed = self.get_feed(feed_id=feed_id)
        if feed is None:
            raise FeedException(code=404, message="Unknown feed", url="")
        else:
            if feed.owner_id != owner.id:
                raise FeedException(code=403, message="This feed doesn't belong to this user", url=feed.url)
            else:
                self._sess.delete(feed)
                self._sess.commit()
                return True

    def publish(self, since_override: datetime.datetime = None):

        mastodon = MastodonService()

        feeds = self.get_feeds()
        for feed in feeds:
            if feed.checked_at is None and since_override is None:
                logger.warning(f"Checking feed {feed.url} from the beginning as checked_at is null")
                since = datetime.datetime(year=1980, month=4, day=29, hour=0, minute=0)
            elif since_override is not None:
                since = since_override
            else:
                logger.info(f"Checking new items on feed {feed.url} since {feed.checked_at}")
                since = feed.checked_at

            logger.info("Fetching items from remote URL")
            content = feedparser.parse(feed.url)



            if "entries" in content and len(content.entries) > 0:
                to_publish = []
                for entry in content.entries:
                    entry_pub_date = datetime.datetime.fromtimestamp(mktime(entry.published_parsed), tz=pytz.UTC)
                    if entry_pub_date > since:
                        logger.info(f"Post '{entry.title}' published on {entry_pub_date} marked")
                        to_publish.append(entry)

                # Entries are chronological, reverse the list then publish it
                to_publish.reverse()
                mastodon.publish(to_publish)

                logger.info(f"{len(to_publish)} entries published.")
            else:
                logger.error("No entries in feed.")

            # Update the feed checked datetime
            feed.checked_at = datetime.datetime.now(tz=pytz.UTC)
            self._sess.commit()


