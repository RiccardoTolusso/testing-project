from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

from .config import DB_URL, DB_NAME, DB_PASSWORD, DB_USER

from typing import Annotated, Optional, List

from fastapi import Depends

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


#### MODELS ####

# USER MODELS
class BaseUser(SQLModel):
    username: str = Field(index=True, unique=True)
    
class User(BaseUser, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str = Field()
    family_id: Optional[int] = Field(default=None, foreign_key="family.id")
    familiy: Optional["Family"] = Relationship(back_populates="users") 

class PublicUser(BaseUser):
    id: int  

class CreateUser(BaseUser):
    password: str 

# FAMILY MODEL
class Family(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None
    users: List["User"] = Relationship(back_populates="family") 
    incomes: List["Income"] = Relationship(back_populates="family")  
    categories: List["Category"] = Relationship(back_populates="family")
    expenses: List["Expense"] = Relationship(back_populates="family")

# INCOME MODEL
class Income(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: int
    description: str | None
    family_id : int | None = Field(default=None, foreign_key="family.id")
    family: Family | None = Relationship(back_populates="incomes")

# CATEGORY MODEL
class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None    
    family_id: int | None = Field(default=None, foreign_key="family.id")
    family: Family | None = Relationship(back_populates="categories")
    expenses: List["Expense"] = Relationship(back_populates="category")

# EXPENSES MODEL
class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: int
    description: str
    family_id: int | None = Field(default=None, foreign_key="family.id")
    category_id: int | None = Field(default=None, foreign_key="category.id")

    family: Family | None = Relationship(back_populates="expenses")
    category: Category | None = Relationship(back_populates="expenses")

#### END MODELS ####

# db connection
def get_session():
    with Session(engine) as session:
        yield session 


SessionDep = Annotated[Session, Depends(get_session)]