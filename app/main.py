import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import List
from pydantic import AnyHttpUrl
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.cron_job import BackgroundRunner
from app.quote import get_iex_quotes




app = FastAPI()
runner = BackgroundRunner()


BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:4200",
        "http://geb.ixx.cc",
        "https://geb.ixx.cc",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def app_startup():
    asyncio.create_task(runner.run_main())



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/quotes")
def get_quotes():
    return JSONResponse(content=get_iex_quotes())
