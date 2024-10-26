#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：demo_schema.py
@Time    ：2023/12/14 15:08
@Desc    ：
"""
from typing import Union, List

from pydantic import BaseModel

from demo_service.models import Author, Book
from demo_service.schemas import GenericSerializerSchemas
from ..libs.fastapi_rest_framework.schemas import BaseResponseListSchema, BaseResponseMode


class AuthorSchema(GenericSerializerSchemas):
    class Meta:
        model = Author

    class PydanticMeta:
        exclude = ("id",)


class QueryAuthorSchema(GenericSerializerSchemas):
    class Meta:
        model = Author

    class PydanticMeta:
        exclude = ()


class ListAuthorSchema(GenericSerializerSchemas):
    class Meta:
        is_many = True
        model = Author

    class PydanticMeta:
        exclude = ()


class CreateBookSchema(GenericSerializerSchemas):
    class Meta:
        is_many = True
        model = Book

    class PydanticMeta:
        exclude = ("id", "author", "author_id")


class UpdateBookSchema(GenericSerializerSchemas):
    class Meta:
        is_many = True
        model = Book

    class PydanticMeta:
        exclude = ("author", "author_id")


class CreateAuthorSchema(AuthorSchema()):
    books: CreateBookSchema()


class UpdateAuthorSchema(AuthorSchema()):
    books: UpdateBookSchema()


class ResponseAuthorSchema(BaseResponseMode):
    data: Union[None, QueryAuthorSchema()]


class ResponseListAuthorSchema(BaseResponseListSchema):
    class ListData(BaseModel):
        data: Union[None, ListAuthorSchema()]
        count: int

    data: ListData
