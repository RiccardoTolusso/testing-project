from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Annotated
from pydantic import BaseModel

import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from passlib.context import CryptContext




#### SETTINGS ####

# jwt settings
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pswd crypt settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth scheme initialization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# fake temporay database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    }
}

#### END SETTINGS ####

router = APIRouter()




#### MODELS ####

# users
class BaseUser(BaseModel):
    username: str
    email: str | None = None

class WithPasswordUser(BaseUser):
    password: str


# tokens
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

#### END MODELS ####

#### FUNCTIONS ####

# password hashing
def get_password_hash(password: str):
    """Gets a string as input and returns the hased value of that string. Used for password hashing"""
    return pwd_context.hash(password)

# password match check
def verify_password(plain_password: str, hashed_password: str):
    """Hashes the plain password to check if it matches the stored hashed password"""
    return pwd_context.verify(plain_password, hashed_password)




#### END FUNCTIONS ####



##### ROUTES ####

# post route to authenticate using email and password to get a valid token
@router.post('/get-token')
async def get_token():
    return "post route to authenticate using email and password to get a valid token"

# post route to create a new user with email and password
@router.post('/register')
async def register_new_user(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return "post route to create a new user with email and password"

# get request to fetch logged user data
@router.get('/me')
async def user_info():
    return "get request to fetch logged user data"

#### END ROUTES ####