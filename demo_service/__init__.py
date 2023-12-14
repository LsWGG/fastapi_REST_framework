#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：__init__.py.py
@Time    ：2023/12/6 11:02
@Desc    ：
"""
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from demo_service.api.router import api_router
from demo_service.db import init_db


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js',
        swagger_css_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css'
    )


def create_app():
    app = FastAPI(
        title="fastapi_REST_framework",
        version="0.1.1",
        docs_url="/api/docs",  # 自定义文档地址
        openapi_url="/api/openapi.json",
    )
    # 引入swagger ui静态文件(解决部分场景下不显示问题)
    app.get_swagger_ui_html = swagger_monkey_patch

    # 导入路由, 前缀设置
    app.include_router(
        api_router
    )

    # 初始化DB
    init_db(app)

    return app
