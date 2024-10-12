from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Annotated
from pydantic import BaseModel

import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from passlib.context import CryptContext

from config import SECRET_KEY


#### SETTINGS ####

# jwt settings
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
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
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


# gets the user with the specified username from the database and returns it with the password
def get_user(db, username: str) -> WithPasswordUser:
    """DO NOT USE THE RETURN OF THIS FUNCTION AS RESPONSE TO A USER REQUEST (PASSWORD EXPOSED). Currently checks inside the dictionary for a username match, next it will use a database"""
    if username in db:
        user_dict = db[username]
        return WithPasswordUser(**user_dict)

# gets the user by username and checks if username and password are right and returns the user with the password
def authenticate_user(fake_db, username: str, password: str):
    """USER WITH PASSWORD EXPOSED. Checks username (using get_user()) and password"""
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# token generation
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """data wants a {"sub": username} dict"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# gets the user from token by decoding the token and using the decoded username to find the right user
async def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError: 
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

#### END FUNCTIONS ####



##### ROUTES ####

# post route to authenticate using email and password to get a valid token
@router.post('/token')
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print("ok")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=new_access_token, token_type="bearer")

# post route to create a new user with email and password
@router.post('/register')
async def register_new_user(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return "post route to create a new user with email and password"

# get request to fetch logged user data
@router.get('/me')
async def user_info():
    return "get request to fetch logged user data"

#### END ROUTES ####