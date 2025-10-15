from fastapi import FastAPI, Path, Query, status, HTTPException
from pydantic import BaseModel, Field
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


#path parameter
@app.get("/robots/{name}/{age}")
async def read_item(name: str, age: int=10):
    return {f"{name} is {age} years old"}

#query parameter
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

#query/path parameter
@app.get("/query-path/{item_id}")
async def read_item(item_id: str, q: str = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

#request body and pydantic

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
 

# path parameters and validation
class User(BaseModel):
    name: str
    age: int = Field(description="user age is between 0-100", ge=0, le=100)
    email: str = Field(description="user email", min_length=3, max_length=50, pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: str = Field(description="user password", min_length=3, max_length=50)


class UserResponse(BaseModel):
    name: str
    email: str

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if user.name == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin is not allowed to register")  
    return user


