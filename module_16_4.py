from fastapi import FastAPI, Path, status, HTTPException
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def post_user(user: User) -> str:
    if users:
        user.id = len(users)
    else:
        user.id = 1
    users.append(user)
    return f"The user with id={user.id} is registered"


@app.put('/user/{user_id}/{username}/{age}')
async def put_user(user_id: Annotated[int, Path(ge=0, le=1000, description="Enter user_id", example='10')],
                    username: Annotated[str, Path(min_length=5, max_length=30, description="Enter username", example="UrbanUser")],
                    age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> str:
    try:
        users[user_id].username = username
        users[user_id].age = age
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
    return users[user_id]


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=0, le=1000, description="Enter user_id", example='10')]) -> str:
    try:
        return users.pop(user_id)
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
