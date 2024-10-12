from fastapi import APIRouter, Form
from typing import Annotated
from pydantic import BaseModel
import os

router = APIRouter()

#### SETTINGS ####

# jwt settings
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#### END SETTINGS ####


#### MODELS ####
class BaseUser(BaseModel):
    email: str

class LoginUser(BaseUser):
    password: str

class RegisterUser(LoginUser):
    pass

class OutputUser(BaseUser):
    pass

#### END MODELS ####


#### FUNCTIONS ####






#### END FUNCTIONS ####



##### ROUTES ####

# post route to authenticate using email and password to get a valid token
@router.post('/get-token')
async def get_token():
    return "post route to authenticate using email and password to get a valid token"

# post route to create a new user with email and password
@router.post('/register')
async def register_new_user(user: Annotated[RegisterUser, Form()]):
    return "post route to create a new user with email and password"

# get request to fetch logged user data
@router.get('/me')
async def user_info():
    return "get request to fetch logged user data"

#### END ROUTES ####