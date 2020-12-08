import asyncpg
import databases

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("database url set to: ", settings.database_url)
database = databases.Database(settings.database_url)

Base = declarative_base()


async def get_db_connection():
    connection = await asyncpg.connect(settings.database_url)
    return connection