from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

class Availability(BaseModel):
    date: datetime
    slots: list[int]

app = FastAPI()

@app.put("/availability")
def put_availability(
    availabilities: list[Availability]
):
    for availability in availabilities:
        availability.slots.sort()
        print(availability)
