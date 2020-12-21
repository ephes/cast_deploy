from typing import Optional

from pydantic import BaseModel


class DeploymentBase(BaseModel):
    title: str
    description: Optional[str] = None


class DeploymentCreate(DeploymentBase):
    pass


class Deployment(DeploymentBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    username: str
    is_active: bool
    deployments: list[Deployment] = []

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str
