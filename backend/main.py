from fastapi import FastAPI
from .logging import CustomizeLogger
from .routers import feeds


# App factory
def create_app():
    _app = FastAPI(title='POSSEbles', debug=False)
    logger = CustomizeLogger.make_logger()
    _app.logger = logger

    # Routers
    _app.include_router(feeds.router)

    return _app


app = create_app()
