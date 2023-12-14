#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：helper.py
@Time    ：2022/3/9 9:20 上午
@Desc    ：
"""
import re

from fastapi import HTTPException
from starlette import status
from tortoise import fields
from tortoise.queryset import QuerySet


def camel_to_snake_case(words: str):
    return re.sub('([A-Z][a-z]+)', r'\1_', words).rstrip('_').lower()


def create_meta_class(model, **kwargs):
    return type("Meta", (), {"model": model, **kwargs})


def is_method_overloaded(cls, method_name) -> bool:
    method = getattr(cls, method_name, False)
    return method and method != getattr(super(cls, cls), method_name, None)


def get_model_foreignkey_field(model) -> list:
    """
    获取模型类的外键字段
    """
    ret = list()
    for k, v in model._meta.fields_map.items():
        if isinstance(v, fields.relational.BackwardFKRelation):
            ret.append(k)
        if isinstance(v, fields.relational.ForeignKeyFieldInstance):
            if v.related_name:
                ret.append(v.related_name)
            else:
                ret.append(f"{model._meta.db_table}s")

    return ret


def get_object_or_404(queryset: QuerySet, is_query, **kwargs):
    if is_query:
        obj = queryset.filter(**kwargs)
    else:
        obj = queryset.filter(**kwargs).first()

    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="数据不存在")

    return obj
