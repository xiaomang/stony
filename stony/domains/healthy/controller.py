from litestar import Controller, get

from stony.domains.healthy.schemas import HealthyResponse


class HealthyController(Controller):
    path = "/healthy"

    @get(summary="健康检查", description="供客户端检查服务是否健康")
    async def find_healthy(self) -> HealthyResponse:
        return HealthyResponse(status=True)
