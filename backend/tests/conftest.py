import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from ..models import User
from ..database import Base
from ..main import app, get_db
from ..auth import get_password_hash


test_client = TestClient(app)
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return test_client


@pytest.fixture
def db():
    return next(get_db())

@pytest.fixture
def password():
    return "password"

@pytest.fixture
def user(db, password):
    kwargs = dict(username="user1", hashed_password=get_password_hash(password), is_active=True)
    user = db.query(User).filter_by(username=kwargs["username"]).first()
    if not user:
        user = User(username="user1", hashed_password=get_password_hash("password"), is_active=True)
        db.add(user)
    return user
