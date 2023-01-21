from fastapi import FastAPI
from .logging import CustomizeLogger


# App factory
def create_app():
    _app = FastAPI(title='CustomLogger', debug=False)
    logger = CustomizeLogger.make_logger()
    _app.logger = logger

    return _app


app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
