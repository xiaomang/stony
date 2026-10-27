from typing import Annotated

from msgspec import Struct


class HealthyResponse(Struct):
    status: Annotated[bool, "是否健康"]
