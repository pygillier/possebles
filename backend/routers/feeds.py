from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import crud, schemas
from backend.dependencies import db, security
import logging
from backend.dependencies import security

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/feeds",
    tags=["Feeds"]
)


@router.post("/", response_model=schemas.Feed)
async def create_feed(
        feed: schemas.FeedCreate,
        current_user: schemas.User = Depends(security.get_current_active_user),
        sess: Session = Depends(db.get_db)
):
    logger.info("Inserting new feed")
    feed = crud.create_user_feed(db=sess,feed=feed, user_id=current_user.id)
    return feed


@router.get("/")
async def read_feeds(skip: int = 0, limit: int = 100, sess: Session = Depends(db.get_db)):
    logger.info("Getting all feeds")
    feeds = crud.get_feeds(sess, skip=skip, limit=limit)
    return feeds


@router.get("/{feed_id}")
async def get_feed(feed_id: str):
    logger.info("Getting feed {}".format(feed_id))
    pass


@router.patch("/{feed_id}")
async def update_feed(feed_id: str):
    logger.info("Updating feed {}".format(feed_id))


@router.delete("/{feed_id}")
async def delete_feed(feed_id: str):
    logger.info("Deleting feed {}".format(feed_id))
    pass
