from fastapi import FastAPI
from .logging import CustomizeLogger
from .routers import feeds
from .settings import app_settings


# App factory
def create_app():
    _app = FastAPI(title='POSSEbles', debug=app_settings.debug)
    logger = CustomizeLogger.make_logger()
    _app.logger = logger

    if app_settings.debug:
        _app.logger.warning("Debug enabled")

    # Routers
    _app.include_router(feeds.router)

    return _app


app = create_app()
