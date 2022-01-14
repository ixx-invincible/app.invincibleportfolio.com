import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import List
from pydantic import AnyHttpUrl
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.cron_job import BackgroundRunner
from app.quote import get_iex_quotes, get_yahoo_quotes, get_live_quote
from app.portfolio import calculate_invincible_portfolio, calculate_invincible_portfolio2
from app.etfs import calculate_etfs



app = FastAPI()
runner = BackgroundRunner()


BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:4200",
        "http://localhost:4201",
        "http://localhost:4202",
        "http://geb.ixx.cc",
        "https://geb.ixx.cc",
        "http://etc.ixx.cc",
        "https://etc.ixx.cc",
        "http://etf.ixx.cc",
        "https://etf.ixx.cc",
        "http://invincibleportfolio.com",
        "https://invincibleportfolio.com",
        "http://www.invincibleportfolio.com",
        "https://www.invincibleportfolio.com",
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
    # return get_yahoo_quotes()


@app.get("/yahoo_quote")
def yahoo_quote():
    get_yahoo_quotes()
    return {"message": "done"}


@app.get("/live_quote")
def live_quote():
    return get_live_quote()
    


@app.get("/invincible_portfolio")
def calculate():
    calculate_invincible_portfolio()
    return {"message": "done"}


@app.get("/invincible_portfolio2")
def calculate2():
    calculate_invincible_portfolio2()
    return {"message": "done"}

@app.get("/etfs")
def calculate_etf():
    calculate_etfs()
    return {"message": "done"}
