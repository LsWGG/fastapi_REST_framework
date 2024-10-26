#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：__init__.py.py
@Time    ：2023/12/7 09:30
@Desc    ：
"""
from demo_service.api.base_api import AuthorViewSet
from demo_service.libs.fastapi_rest_framework.router import MainRouter

routers = [
    MainRouter(prefix="/author", tags=["作者"]).is_view(AuthorViewSet),
]
