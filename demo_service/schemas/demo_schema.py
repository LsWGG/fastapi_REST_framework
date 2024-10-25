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
from demo_service.schemas import GenericSerializerSchemas, BaseResponseMode, BaseResponseListSchema


class AuthorSchema(GenericSerializerSchemas):
    class Meta:
        model = Author


class BookSchema(GenericSerializerSchemas):
    class Meta:
        model = Book


class BookS(BookSchema):
    title: str
    published_date: str


class CreateOrUpdateAuthorSchema(AuthorSchema):
    books: List[BookS]

    class PydanticMeta:
        exclude = (
            "id", "created_at", "updated_at"
        )


class CreateOrUpdateBookSchema(BookSchema):
    class PydanticMeta:
        exclude = ("id", "created_at", "updated_at")


class ListAuthorSchema(AuthorSchema):
    class Meta:
        is_many = True
        model = Author


class ListBookSchema(BookSchema):
    class Meta:
        is_many = True
        model = Book


class ResponseAuthorSchema(BaseResponseMode):
    data: Union[None, AuthorSchema()]


class ResponseBookSchema(BaseResponseMode):
    data: Union[None, BookSchema()]


class ResponseListAuthorSchema(BaseResponseListSchema):
    class ListData(BaseModel):
        data: Union[None, ListAuthorSchema()]
        count: int

    data: ListData


class ResponseListBookSchema(BaseResponseListSchema):
    class ListData(BaseModel):
        data: Union[None, ListBookSchema()]
        count: int

    data: ListData
