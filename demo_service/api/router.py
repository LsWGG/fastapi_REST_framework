# -*- coding: utf-8 -*-
# Time : 2022/5/9 15:10
# Author: Gynine
# Email: gaoyongjiu@stonehg.com
__doc__ = """
    实现路由检测功能，需在app组件__init__.py内定义 app_name + _router和app_name + _tags 属性
    20220512：增加了白名单配置 app_name + _white_list
    示例（*为必选）：
        example_tags = ["测试"]
        *example_router = APIRouter()
        example_white_list = []
"""
import importlib
import os.path

from fastapi import APIRouter

from demo_service.settings import settings

api_router = APIRouter()

obj = importlib.import_module("demo_service.api")

router_key = "routers"
if isinstance(getattr(obj, router_key), list):
    for router in getattr(obj, router_key):
        api_router.include_router(router)
else:
    api_router.include_router(getattr(obj, router_key))
