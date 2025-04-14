import logging
from fastapi import FastAPI
from pygments.lexers import templates
from starlette.requests import Request
from contextlib import asynccontextmanager
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from models.db_main import create_database, create_tables
from routers import tables


logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logger = logging.getLogger("app")



async def lifespan(app: FastAPI):
    logger.info("Startup event triggered")
    await create_database()
    await create_tables()
    yield
    logger.info("Shutdown event triggered")


app = FastAPI(lifespan=lifespan)

app.include_router(tables.router)


@app.middleware("http")
async def log_request(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
