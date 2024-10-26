#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：user_model.py
@Time    ：2023/12/6 18:06
@Desc    ：
"""
from tortoise import fields
from tortoise.models import Model


class Author(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    name = fields.CharField(max_length=255, unique=True)
    books = fields.ReverseRelation['Book']

    class Meta:
        table = "author"
        table_description = "作者信息表"

    def __str__(self):
        return self.name


class Book(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    title = fields.CharField(max_length=255, unique=True)
    author = fields.ForeignKeyField(
        'models.Author', related_name='books', on_delete=fields.SET_NULL, null=True
    )

    class Meta:
        table = "book"
        table_description = "书籍信息表"

    def __str__(self):
        return self.title
