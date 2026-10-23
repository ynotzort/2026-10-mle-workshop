import random

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def ping():
    return "PONG"


@app.get("/random")
def random_number():
    return random.randint(1,10)
