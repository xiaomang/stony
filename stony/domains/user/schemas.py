from typing import Annotated

from bson import ObjectId
from msgspec import UNSET, Meta, Struct


class UserFindResponse(Struct):
    id: Annotated[ObjectId, Meta(description="用户ID")]
    username: Annotated[str, Meta(description="用户名")]
    created_at: Annotated[str, Meta(description="创建时间")]
    client_ip: Annotated[str, Meta(description="客户端IP")]


class UserCreateRequest(Struct):
    username: Annotated[str, Meta(description="用户名", min_length=2, max_length=20)]
    password: Annotated[str, Meta(description="密码", min_length=8, max_length=20)]


class UserCreateResponse(Struct):
    id: Annotated[ObjectId, Meta(description="用户ID")] = UNSET
    username: Annotated[str, Meta(description="用户名")] = UNSET
    created_at: Annotated[str, Meta(description="创建时间")] = UNSET
    client_ip: Annotated[str, Meta(description="客户端IP")] = UNSET
