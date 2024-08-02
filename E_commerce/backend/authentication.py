from typing import Union, Any,Text
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from pydantic import BaseModel
from jose import jwt
from pydantic import ValidationError
from database import SessionLocal
import models

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/user_login/",
    scheme_name="JWT"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TokenPayload(BaseModel):
    exp:int
    sub:str
    
class SystemUser(BaseModel):
    username:str

def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    db = next(get_db())
    user = db.query(models.User).filter(models.User.email == (token_data.sub)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    user = SystemUser(username=user.username)
    return user

