from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str 
    password: str = Field(min_length=3, max_length=50)
    age: int = Field(default=18)