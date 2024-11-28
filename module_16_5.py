from fastapi import FastAPI, Path, status, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()

users = []
templates = Jinja2Templates(directory='templates')


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})


@app.post('/user/{username}/{age}')
async def post_user(user: User) -> str:
    if users:
        user.id = max(users, key=lambda urs: urs.id).id + 1
    else:
        user.id = 1
    users.append(user)
    return f"The user with id={user.id} is registered"


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=0, le=1000, description="Enter user_id", example='10')],
                    username: Annotated[str, Path(min_length=5, max_length=30, description="Enter username", example="UrbanUser")],
                    age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> str:
    try:
        users[user_id - 1].username = username
        users[user_id - 1].age = age
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
    return users[user_id]


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=0, le=1000, description="Enter user_id", example='10')]) -> str:
    try:
        return users.pop(user_id - 1)
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")