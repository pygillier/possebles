from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import crud
from backend.dependencies.db import get_db
import logging
from backend.dependencies import security

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/feeds",
    tags=["Feeds"],
    dependencies=[Depends(security.oauth2_scheme)]
)

@router.post("/")
async def create_feed():
    logger.info("Inserting new feed")
    pass


@router.get("/")
async def read_feeds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting all feeds")
    feeds = crud.get_feeds(db, skip=skip, limit=limit)
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
