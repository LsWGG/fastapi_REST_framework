#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：api.py
@Time    ：2023/12/6 10:54
@Desc    ：
"""
from libs.fastapi_rest_framework.schemas import BaseResponseMode
from libs.fastapi_rest_framework.viewsets import ModelViewSet

from ..models import Author
from ..schemas.demo_schema import (
    AuthorSchema,
    ResponseAuthorSchema,
    CreateAuthorSchema,
    UpdateAuthorSchema,
    ResponseListAuthorSchema,
    QueryAuthorSchema
)


class AuthorViewSet(ModelViewSet):
    """
    作者增删改查
    """
    # 数据库模型类
    model = Author
    # generic_schema = GenericSerializerSchemas

    # Schema类：请求参数校验
    schema_class = QueryAuthorSchema
    create_schema_class = CreateAuthorSchema
    update_schema_class = UpdateAuthorSchema

    # 响应模型：定义响应格式
    response_model = BaseResponseMode
    list_response_model = ResponseListAuthorSchema
    retrieve_response_model = ResponseAuthorSchema
