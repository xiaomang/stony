import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from litestar import Litestar
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from stony.settings import Settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def mongo_db_lifespan(
    app: Litestar,
) -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """应用程序生命周期管理"""
    settings: Settings = app.state["settings"]
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client[settings.mongo_db_name]
    logger.info(f"Connected to MongoDB: {settings.mongo_uri}")
    app.state["mongo_db"] = db
    yield
    client.close()
    logger.info("MongoDB connection closed")


async def set_mongo_index_on_startup(app: Litestar) -> None:
    """在 MongoDB 启动时设置索引"""
    db = app.state["mongo_db"]
    await db.create_index("username", unique=True)
