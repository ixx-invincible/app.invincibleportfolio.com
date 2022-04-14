import random

import asyncio

from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from typing import List
from pydantic import AnyHttpUrl
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.cron_job import BackgroundRunner
from app.quote import get_iex_quotes, get_yahoo_quotes, get_live_quote
from app.portfolio import calculate_invincible_portfolio, calculate_invincible_portfolio2
from app.etfs import calculate_etfs
from app.smart_marksix import send_marksix



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


# @app.get("/send-smart-marksix/{email}")
# async def send_smart_marksix(email: str, background_tasks: BackgroundTasks):
    
#     send_marksix(email, background_tasks)
    
#     return {"message": "Notification sent in the background"}

    

@app.get("/smart-marksix")
async def get_smart_marksix():
    random_list = random.sample(range(13, 50), 37)

    random_pos = random.sample(range(0, 36), 5)

    for i in random_pos:
        random_list.append(random_list[i])

    tickets = []

    for i in range(7):
        tickets.append(random_list[i*6:(i+1)*6])
    
    return tickets


@app.get("/smart-marksix/{banker}")
async def get_smart_marksix(banker: int):
    random_list = random.sample(range(13, 50), 37)

    random_list.remove(banker)

    random_pos = random.sample(range(0, 36), 5)

    for i in random_pos:
        random_list.append(random_list[i])

    tickets = []

    for i in range(8):
        ticket = random_list[i*5:(i+1)*5]
        ticket.insert(0, banker)

        tickets.append(ticket)
    
    return tickets