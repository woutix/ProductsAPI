from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from logging import Logger

from router import router
from database import database as db


@asynccontextmanager
async def lifespan(app: FastAPI):
   logger = Logger
   await db.create_tables()
   logger.info("База готова")
   yield
   await db.delete_tables()
   logger.info("База очищена")

app = FastAPI(lifespan=lifespan)
app.include_router(router)
