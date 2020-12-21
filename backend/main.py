import asyncio
import subprocess

from typing import List, Optional
from datetime import timedelta

from asyncpg import Connection
from pydantic import BaseModel
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from fastapi import Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks, FastAPI, WebSocket, WebSocketDisconnect

from . import crud, models, schemas, auth, repository
from .config import settings
from .repository import DatabasesRepository
from .database import SessionLocal, engine, database, get_db_connection

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="backend/templates")
print("set_db with url: ", settings.database_url)
repository.set_db(repository.DatabasesRepository(settings.database_url))


# @app.get("/users/me/deployments/")
# async def read_own_deployments(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    db = repository.get_db()
    await db.connect()
    print("startup async databases repo: ", db)


@app.on_event("shutdown")
async def shutdown():
    db = repository.get_db()
    await db.disconnect()


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    import os

    print(os.getcwd())
    return templates.TemplateResponse("deploy.html", {"request": request, "counter": "{{ counter }}"})


@app.get("/hello")
async def get():
    return {"message": "hello from fastapi"}


@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: repository.AbstractRepository = Depends(repository.get_db)):
    users = await db.list_users(skip=skip, limit=limit)
    return users


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: repository.AbstractRepository = Depends(repository.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/me")
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Connection = Depends(repository.get_db)
):
    # user_row = await crud.aget_user_by_name(db, form_data.username)
    user = await auth.authenticate_user(db, form_data.username, form_data.password)
    print("user: ", user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


async def run_deploy():
    print("running deployment")
    proc = await asyncio.create_subprocess_shell(
        "./deploy_cast_hosting.sh",
        # "./sample.sh",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    while True:
        data = await proc.stdout.readline()
        if len(data) == 0:
            break

        data = data.decode("UTF-8")
        print("data: ", data, end="")
        await manager.broadcast(data)

    print("return code:", proc.returncode)
    print("deployment complete")


@app.post("/deploy")
async def deploy(background_tasks: BackgroundTasks):
    print("received deploy event")
    background_tasks.add_task(run_deploy)
    return {"message": "deploying"}
