from litestar import Request
from litestar.datastructures import State
from motor.motor_asyncio import AsyncIOMotorDatabase


async def provide_mongo_db(state: State) -> AsyncIOMotorDatabase:
    """提供MongoDB数据库依赖"""
    return state["mongo_db"]


async def provide_client_ip(request: Request) -> str:
    """提供客户端IP依赖"""
    return request.client.host
