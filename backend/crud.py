from .models import Deployment
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


async def get_async_users(db):
    user_schema = schemas.User
    query = models.User.__table__.select()
    return [user_schema(**row) for row in await db.fetch_all(query)]


async def aget_user_by_name(db, username):
    stmt = await db.prepare("select * from users where username = $1")
    return await stmt.fetchrow(username)


def get_user_by_name(db, username):
    return db.query(models.User).filter_by(username=username).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_deployments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Deployment).offset(skip).limit(limit).all()


def create_user_deployment(db: Session, deployment: schemas.DeploymentCreate, user_id: int):
    db_deployment = models.Deployment(**deployment.dict(), owner_id=user_id)
    db.add(db_deployment)
    db.commit()
    db.refresh(db_deployment)
    return db_deployment
