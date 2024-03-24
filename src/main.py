from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
import os
import uvicorn
from dto.Availability import AvailabilityDTO
from dto.User import UserDTO
from dto.Response import ResponseDTO
import jwt
from datetime import datetime

load_dotenv()
app = FastAPI()

JWT_ALGORITHMS = "HS256"

@app.middleware("http")
async def auth_middleware(request: Request, call_next):

    if 'auth' in request.url._url:
        return await call_next(request)
    
    token = request.headers.get('Authorization', '')    
    try:
        jwt.decode(
            jwt=token.replace("Bearer ", ""),
            key=os.environ['JWT_SECRET'],
            algorithms=JWT_ALGORITHMS
        )
    except Exception as e:
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder(ResponseDTO(message="Invalid token"))
        )

    response = await call_next(request)
    return response

@app.put("/auth/register")
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
    

@app.get("/auth/login")
def login(user: UserDTO):
    # todo aggiungere controllo utente in database
    return ResponseDTO(
        message="Successfully logged in",
        data={
            "token": jwt.encode(
                payload={"username": user.username, "created_at": datetime.now().timestamp()},
                key=os.environ['JWT_SECRET'],
                algorithm=JWT_ALGORITHMS
            )
        })

@app.put("/availability")
def put_availability(
    availabilities: list[AvailabilityDTO]
):
    for availability in availabilities:
        availability.slots.sort()
        print(availability)

    return ResponseDTO(
        message="Availability set"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ["SERVER_PORT"]))