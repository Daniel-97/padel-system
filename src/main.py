from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import uvicorn
from dto.Availability import AvailabilityDTO
from dto.User import UserDTO
from dto.Response import ResponseDTO
import jwt

load_dotenv()
app = FastAPI()

@app.put("/register")
def register(user: UserDTO):

    if user.username == '':
        raise HTTPException(
            status_code=400,
            detail="Invalid username"    
        )

    if user.password == '':
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )
    
    # TODO add user to database
    
    return ResponseDTO(message=f"User {user.username} successfully registered!")
    

@app.get("/login")
def login(user: UserDTO):
    pass

@app.put("/availability")
def put_availability(
    availabilities: list[AvailabilityDTO]
):
    for availability in availabilities:
        availability.slots.sort()
        print(availability)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ["SERVER_PORT"]))