import abc

from databases import Database

# from . import models
from . import schemas


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: schemas.User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> schemas.User:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add_user(self, user):
        self.session.add(user)

def get_user_by_name(db, username):
    return db.query(models.User).filter_by(username=username).first()

    def get_user(self, username):
        return self.session.query(models.User).filter_by(username=username).one()

    def list_users(self):
        return self.session.query(models.User).all()


class FakeRepository(AbstractRepository):
    def __init__(self, users, deployments):
        self._users = set(users)
        self._deployments = set(deployments)

    def add_user(self, user):
        self._users.add(user)

    def get_user(self, username):
        return next(u for u in self._users if u.username == username)

    def list_users(self):
        return list(self._users)


class DatabasesRepository(AbstractRepository):
    def __init__(self, database_url):
        self.db = Database(database_url)

    async def connect(self):
        await self.db.connect()
    
    async def disconnect(self):
        await self.db.disconnect()

    async def add_user(self, user):
        query = (
            "INSERT INTO users(id, username, is_active)"
            " VALUES (:id, :username, :is_active)"
        )
        user_dict = user.dict()
        del user_dict["deployments"]
        values = [user_dict]
        await self.db.execute_many(query=query, values=values)

    async def get_user(self, username):
        query = "select * from users where username = :username"
        user = await self.db.fetch_one(query, values={"username": username})
        return schemas.User(**dict(user))

    async def list_users(self):
        query = "select * from users"
        users = await self.db.fetch_all(query)
        return [schemas.User(**dict(user)) for user in users]
