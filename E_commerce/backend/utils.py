import os
from typing import Union,Any
from datetime import datetime,timedelta
from jose import jwt

JWT_SECRET_KEY = "SUPERCOOL"
JWT_REFRESH_SECRET_KEY = "SUPERFUN"
JWT_CARD_SECRET_KEY = "HEYTHERE"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60*24*7
ALGORITHM = "HS256"
JWT_SECRET_KEY=JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY=JWT_REFRESH_SECRET_KEY
JWT_CARD_SECRET_KEY =JWT_CARD_SECRET_KEY


def create_access_token(subject: Union[str, Any],expires_delta:int  =None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any],expires_delta:int=None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def cardno_token(subject: Union[str, Any]) -> str:
    to_encode = {"sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode,JWT_CARD_SECRET_KEY,ALGORITHM)
    print(f"Subject: {subject}")
    return encoded_jwt