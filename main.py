from fastapi import FastAPI
import uvicorn
from models.db_main import create_database, create_tables

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await create_database()
    await create_tables()


@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
