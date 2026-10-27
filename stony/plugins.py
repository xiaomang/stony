from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bson import ObjectId
from litestar.openapi.spec import OpenAPIType, Schema
from litestar.plugins import OpenAPISchemaPlugin

if TYPE_CHECKING:
    from litestar._openapi.schema_generation import SchemaCreator
    from litestar.typing import FieldDefinition


class ObjectIdSchemaPlugin(OpenAPISchemaPlugin):
    """将 ObjectId 描述为 OpenAPI 的字符串类型"""

    @staticmethod
    def is_plugin_supported_type(value: Any) -> bool:
        return value is ObjectId

    def to_openapi_schema(
        self,
        field_definition: FieldDefinition,
        schema_creator: SchemaCreator,
    ) -> Schema:
        return Schema(type=OpenAPIType.STRING, pattern=r"^[0-9a-f]{24}$")
