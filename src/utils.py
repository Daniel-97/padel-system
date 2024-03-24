import jwt
import os
from fastapi import HTTPException, status

def check_token(token: str):
    try:
        token_data = jwt.decode(
            jwt=token.replace("Bearer ", ""),
            key=os.environ['JWT_SECRET'],
            algorithms="HS256"
        )
        return token_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )