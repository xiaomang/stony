import asyncio
from datetime import datetime, timezone
from typing import Annotated

import bcrypt
from bson import ObjectId
from litestar import Controller, get, post
from litestar.di import NamedDependency
from litestar.exceptions import HTTPException
from litestar.pagination import OffsetPagination
from litestar.params import QueryParameter
from motor.motor_asyncio import AsyncIOMotorDatabase

from stony.domains.user.schemas import (
    UserCreateRequest,
    UserCreateResponse,
    UserFindResponse,
)


def parse_user(doc: dict) -> UserFindResponse:
    return UserFindResponse(
        id=doc["_id"],
        username=doc["username"],
        created_at=doc["created_at"],
        client_ip=doc["client_ip"],
    )


class UserController(Controller):
    path = "/users"

    @get(summary="获取用户列表")
    async def find(
        self,
        db: NamedDependency[AsyncIOMotorDatabase],
        offset: Annotated[int, QueryParameter(ge=0, le=100)] = 0,
        limit: Annotated[int, QueryParameter(ge=1, le=100)] = 10,
    ) -> OffsetPagination[UserFindResponse]:
        query = {}
        sort = {"created_at": -1}
        projection = {"_id": 1, "username": 1, "created_at": 1, "client_ip": 1}
        total = await db.users.count_documents(query)
        docs = await db.users.find(
            query, projection=projection, skip=offset, limit=limit, sort=sort
        ).to_list()
        items = [parse_user(e) for e in docs]
        return OffsetPagination(
            items=items,
            total=total,
            offset=offset,
            limit=limit,
        )

    @post(summary="创建用户")
    async def create(
        self,
        data: UserCreateRequest,
        db: NamedDependency[AsyncIOMotorDatabase],
        client_ip: NamedDependency[str],
    ) -> UserCreateResponse:
        # 验证用户名是否存在
        entry = await db.users.find_one({"username": data.username})
        if entry:
            raise HTTPException(status_code=409, detail="用户名已存在")
        hashed_password = await asyncio.to_thread(
            bcrypt.hashpw,
            data.password.encode("utf-8"),
            bcrypt.gensalt(),
        )
        doc = {
            "username": data.username,
            "password": hashed_password,
            "created_at": datetime.now(timezone.utc),
            "client_ip": client_ip,
        }
        await db.users.insert_one(doc)
        return UserCreateResponse(
            id=doc["_id"],
            username=doc["username"],
            created_at=doc["created_at"],
            client_ip=doc["client_ip"],
        )
