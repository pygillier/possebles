from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/feeds",
    tags=["Feeds"]
)


@router.get("/")
async def get_feeds():
    logger.info("Getting all feeds")
    pass

@router.get("/{feed_id}")
async def get_feed(feed_id: str):
    logger.info("Getting feed {}".format(feed_id))
    pass


@router.post("/")
async def new_feed():
    logger.info("Inserting new feed")
    pass

@router.patch("/{feed_id}")
async def update_feed(feed_id: str):
    logger.info("Updating feed {}".format(feed_id))
    pass


@router.delete("/{feed_id}")
async def delete_feed(feed_id: str):
    logger.info("Deleting feed {}".format(feed_id))
    pass
