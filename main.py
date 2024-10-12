print("Applicazione avviata, buon apprendimento!")
from typing import Annotated
from fastapi import FastAPI, Query, Depends

from routers import users

app = FastAPI()

app.include_router(
    users.router,
    prefix= "/auth",
    tags=['auth']
    )

# @app.get("/")
# async def root(user: Annotated[BaseUser, Query()]):
#     return {"email": user.email, "password":user.password}

# @app.get("/{message}")
# async def custom_message(message: str):
#     return {"message": message}