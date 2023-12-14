import os
from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    __doc__ = "开发环境配置"

    # ---------------- apps 配置 ----------------
    APP_NAME: str = "fastapi_REST_framework"
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 日志目录
    LOG_PATH: str = os.path.join(BASE_DIR, "logs")
    # 静态文件目录
    STATIC_PATH: str = os.path.join(BASE_DIR, "static")

    # --------------- 跨域配置 ------------------
    # 跨域设置 验证 list包含任意http url
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost']

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_dev_settings():
    """"
    即使加载.env文件，pydantic 依然选择先加载环境变量配置
    """
    return Settings(_env_file="./settings/env_config/dev.env", _env_file_encoding="utf-8")
