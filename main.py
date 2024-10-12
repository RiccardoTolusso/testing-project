print("Applicazione avviata, buon apprendimento!")
from typing import Annotated
from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel

app = FastAPI()

class BaseUser(BaseModel):
    email: str
    password: str
    name: str | None = None

@app.get("/")
async def root(user: Annotated[BaseUser, Query()]):
    return {"email": user.email, "password":user.password}

@app.get("/{message}")
async def custom_message(message: str):
    return {"message": message}