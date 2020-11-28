from typing import List, Optional

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
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    deployments: List[Deployment] = []

    class Config:
        orm_mode = True
