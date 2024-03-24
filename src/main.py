from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

class Availability(BaseModel):
    date: datetime
    slots: list[int]

class User(BaseModel):
    username: str
    password: str

app = FastAPI()


@app.put("/register")
def register(user: User):
    print(user)

@app.get("/login")
def login(user: User):
    pass

@app.put("/availability")
def put_availability(
    availabilities: list[Availability]
):
    for availability in availabilities:
        availability.slots.sort()
        print(availability)
