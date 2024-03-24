from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
import os
import uvicorn
from datetime import datetime
import jwt

from dto.Availability import AvailabilityDTO
from dto.User import UserDTO
from dto.Response import ResponseDTO
from service.DatabaseService import add_user, get_user, add_availability, get_slots, get_user_by_slot

JWT_ALGORITHMS = "HS256"
load_dotenv()
app = FastAPI()

@app.middleware("http")
async def auth_middleware(request: Request, call_next):

    #todo sistemare
    if 'auth' in request.url._url or 'doc' in request.url._url:
        return await call_next(request)
    
    token = request.headers.get('Authorization', '')    
    try:
        token_data = jwt.decode(
            jwt=token.replace("Bearer ", ""),
            key=os.environ['JWT_SECRET'],
            algorithms=JWT_ALGORITHMS
        )
        request.state.token_data = token_data
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder(ResponseDTO(message="Invalid token"))
        )

    response = await call_next(request)
    return response

@app.put("/auth/register")
def register(user: UserDTO):

    if user.username == '':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username"    
        )

    if user.password == '':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password"
        )
    
    if add_user(username=user.username, password=user.password):
        return ResponseDTO(
            message=f"User {user.username} successfully registered!"
        )
    else: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Username already used"
        )
    

@app.get("/auth/login")
def login(dto: UserDTO):
    user = get_user(username=dto.username)
    if user is None or dto.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return ResponseDTO(
        message="Successfully logged in",
        data={
            "token": jwt.encode(
                payload={
                    "username": user.username,
                    "user_id": user.id,
                    "created_at": datetime.now().timestamp()
                },
                key=os.environ['JWT_SECRET'],
                algorithm=JWT_ALGORITHMS
            )
        })

@app.put("/availability")
def put_availability(availabilities: list[AvailabilityDTO], request: Request):

    token_data = request.state.token_data
    user_id = token_data['user_id']

    for availability in availabilities:
        for slot in availability.slots:
            add_availability(user_id=user_id, date=availability.date, slot=slot)

    slots = get_slots()
    for slot in slots:
        users = get_user_by_slot(date=slot.date, hour=slot.hour)
        for user in users:
            print(f'Send email to user {user.username} for slot {slot.date} at {slot.hour}')
            # todo add callback function for user alert

    return ResponseDTO(
        message="Availability set"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ["SERVER_PORT"]))