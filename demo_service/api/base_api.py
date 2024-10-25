#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：api.py
@Time    ：2023/12/6 10:54
@Desc    ：
"""
from ..libs.fastapi_rest_framework.viewsets import ModelViewSet
from ..models import Author, Book
from ..schemas.demo_schema import (
    AuthorSchema,
    ResponseAuthorSchema,
    CreateOrUpdateAuthorSchema,
    ResponseListAuthorSchema,
    BookSchema,
    ResponseBookSchema,
    CreateOrUpdateBookSchema,
    ResponseListBookSchema,
)


class AuthorViewSet(ModelViewSet):
    """
    作者增删改查
    """
    # 数据库模型类
    model = Author

    # Schema类：请求参数校验
    schema_class = AuthorSchema
    create_schema_class = CreateOrUpdateAuthorSchema
    update_schema_class = CreateOrUpdateAuthorSchema

    # 响应模型：定义响应格式
    response_model = ResponseAuthorSchema
    list_response_model = ResponseListAuthorSchema


class BookViewSet(ModelViewSet):
    """
    书籍增删改查
    """
    # 数据库模型类
    model = Book

    # Schema类：请求参数校验
    schema_class = BookSchema
    create_schema_class = CreateOrUpdateBookSchema
    update_schema_class = CreateOrUpdateBookSchema

    # 响应模型：定义响应格式
    response_model = ResponseBookSchema
    list_response_model = ResponseListBookSchema
