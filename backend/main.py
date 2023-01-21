from fastapi import FastAPI
from .logging import CustomizeLogger
from .routers import feeds, users, auth
from .settings import app_settings
from .database import models, engine


# App factory
def create_app():
    _app = FastAPI(title='POSSEbles', debug=app_settings.debug)
    logger = CustomizeLogger.make_logger()
    _app.logger = logger

    if app_settings.debug:
        _app.logger.warning("Debug enabled")

    models.Base.metadata.create_all(bind=engine)
    _app.logger.info("Database mapped")

    # Routers
    _app.include_router(auth.router)
    _app.include_router(users.router)
    _app.include_router(feeds.router)
    _app.logger.info("Routers loaded.")

    return _app


app = create_app()
