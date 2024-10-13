from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

from .config import DB_URL, DB_NAME, DB_PASSWORD, DB_USER

from typing import Annotated

from fastapi import Depends

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# children = Relationship("OtherModelName", back_populates="otherModelAttribute")
class BaseUser(SQLModel):
    username: str = Field(index=True, unique=True)
    
class User(BaseUser, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str = Field()

class PublicUser(BaseUser):
    id: int  

class CreateUser(BaseUser):
    password: str 


# db connection
def get_session():
    with Session(engine) as session:
        yield session 


SessionDep = Annotated[Session, Depends(get_session)]