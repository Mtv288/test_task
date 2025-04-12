import logging
from fastapi import FastAPI
from starlette.requests import Request
from contextlib import asynccontextmanager
from models.db_main import create_database, create_tables


logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Startup event triggered")
    await create_database()
    await create_tables()
    yield
    logger.info("Shutdown event triggered")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_request(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


@app.get("/")
async def read_root():
    return {"message": "Привет, поехали))"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
