from typing import Any

from bson import ObjectId
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.datastructures import State
from litestar.di import Provide
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import (
    JsonRenderPlugin,
    RedocRenderPlugin,
    YamlRenderPlugin,
)

from stony.dependencies import provide_client_ip, provide_mongo_db
from stony.domains.healthy.controller import HealthyController
from stony.domains.user.controller import UserController
from stony.lifespan import mongo_db_lifespan
from stony.plugins import ObjectIdSchemaPlugin
from stony.settings import Settings

# 初始化应用程序配置
settings = Settings()
state = State({"settings": settings})

# 定义路由处理函数
route_handlers = [HealthyController, UserController]

# 配置CORS
cors_config = CORSConfig(allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# 配置应用程序生命周期管理
lifespan = [mongo_db_lifespan]

# 配置依赖注入
dependencies = {
    "db": Provide(provide_mongo_db),
    "client_ip": Provide(provide_client_ip),
}

# 配置类型编码器，将 ObjectId 转换为字符串
type_encoders = {
    ObjectId: str,
}

# 配置 OpenAPI 文档（Redoc 3 为 ESM 包，固定使用 2.x 的 UMD 版本以兼容经典 script 标签）
openapi_config = OpenAPIConfig(
    title="Litestar API",
    version="1.0.0",
    render_plugins=[
        RedocRenderPlugin(
            js_url="https://fastly.jsdelivr.net/npm/redoc@2.5.0/bundles/redoc.standalone.js"
        ),
        JsonRenderPlugin(),
        YamlRenderPlugin(),
    ],
)

app = Litestar(
    debug=settings.debug,
    route_handlers=route_handlers,
    state=state,
    cors_config=cors_config,
    lifespan=lifespan,
    dependencies=dependencies,
    type_encoders=type_encoders,
    openapi_config=openapi_config,
    plugins=[ObjectIdSchemaPlugin()],
)
