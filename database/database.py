from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from database.models import BaseModel


class Database:
    def __init__(self):
        self.__database_url = "postgresql+asyncpg://postgres:@localhost:5432/postgres" # TODO: вынести в конфиг
        self.__engine = create_async_engine(self.__database_url, echo=True)

    async def create_tables(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    async def delete_tables(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)

    def new_session(self):
        return async_sessionmaker(self.__engine, expire_on_commit=False)

database = Database()
