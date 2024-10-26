#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：__init__.py.py
@Time    ：2023/12/14 15:07
@Desc    ：
"""

from typing import (
    Union,
)

from tortoise.contrib.pydantic import PydanticModel

from demo_service.libs.fastapi_rest_framework.schemas import BaseSerializerSchemas
from settings import settings


class GenericSerializerSchemas(BaseSerializerSchemas):
    __doc__ = "用于初始化Model，维护关联关系"

    @classmethod
    def get_models_paths(cls):
        return ['demo_service.models']
