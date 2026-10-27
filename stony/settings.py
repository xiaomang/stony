from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用程序配置"""

    debug: bool = False  # 是否开启调试模式

    # MongoDB配置
    mongo_uri: str = "mongodb://localhost:27017/stony"  # MongoDB连接URI
    mongo_db_name: str = "stony"  # MongoDB数据库名称

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
