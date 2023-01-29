import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from backend.database import schemas
from backend.settings import app_settings
from backend.services.feeds import FeedService
from backend.dependencies import security

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/feeds",
    tags=["Feeds"],
    dependencies=[Depends(security.get_current_active_user)]
)


@router.get("/", response_model=list[schemas.Feed])
async def read_feeds(
        skip: int = 0,
        limit: int = 100,
        svc: FeedService = Depends()
):
    logger.info("Getting all feeds")
    _feeds = svc.get_feeds(skip=skip, limit=limit)
    return _feeds


@router.post("/import", response_model=schemas.Feed)
async def import_feed(
        feed: schemas.FeedImport,
        svc: FeedService = Depends(),
        current_user: schemas.User = Depends(security.get_current_active_user),
):
    logger.info("Importing URL %s" % feed.url)
    _feed = svc.import_feed(url=feed.url, owner=current_user)

    return _feed


##### TESTING ####
@router.get("/publish")
async def check_feeds(
        svc: FeedService = Depends()
):
    if app_settings.debug is False:
        raise HTTPException(
            status_code=403,
        )

    svc.publish()


@router.get("/{feed_id}", response_model=schemas.Feed)
async def get_feed(
        feed_id: int,
        svc: FeedService = Depends()
):
    return svc.get_feed(feed_id=feed_id)


@router.patch("/{feed_id}")
async def update_feed(feed_id: str):
    logger.info("Updating feed {}".format(feed_id))


@router.delete("/{feed_id}")
async def delete_feed(
        feed_id: int,
        current_user: schemas.User = Depends(security.get_current_active_user),
        svc: FeedService = Depends()
):
    logger.info("Deleting feed {}".format(feed_id))

    svc.delete_feed(feed_id=feed_id, owner=current_user)
    return JSONResponse(
        status_code=204,
        content={"message": "Feed deleted"},
    )


