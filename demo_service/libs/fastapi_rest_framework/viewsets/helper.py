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
from tortoise import fields, Tortoise
from tortoise.queryset import QuerySet
from tortoise.models import Model


def camel_to_snake_case(words: str):
    return re.sub('([A-Z][a-z]+)', r'\1_', words).rstrip('_').lower()


def create_meta_class(model, **kwargs):
    return type("Meta", (), {"model": model, **kwargs})


def is_method_overloaded(cls, method_name) -> bool:
    method = getattr(cls, method_name, False)
    return method and method != getattr(super(cls, cls), method_name, None)


def get_backward_rel_keys(model) -> list:
    """
    获取模型类的反向关系字段名
    """
    ret = list()
    for k, v in model._meta.fields_map.items():
        if isinstance(v, fields.relational.BackwardFKRelation):
            ret.append(k)

    return ret


def get_backward_rel(model) -> list:
    """
    获取模型类的反向关系
    """
    ret = list()
    for k, v in model._meta.fields_map.items():
        if isinstance(v, fields.relational.BackwardFKRelation):
            ret.append(v)

    return ret


def get_foreign_key(model, backward_name: str = None) -> str:
    """
    获取模型类的外键字段
    """
    ret = ""
    for k, v in model._meta.fields_map.items():
        if isinstance(v, fields.relational.ForeignKeyFieldInstance):
            if backward_name and v.related_name == backward_name:
                ret = f"{k}_id"

    return ret


def get_model_name(self_model: Model, rel_key: str) -> Model:
    """
    根据传入Schema获取对应Model类名
    :param self_model: 当前model
    :param rel_key 关系字段名
    :return: Model类名
    """
    return getattr(self_model, rel_key).fget.keywords.get('ftype').__name__


def get_model(model_name: str):
    """
    获取模型类
    :param model_name: 模型类名
    :return: 模型类
    """
    return Tortoise.apps['models'].get(model_name)


def get_object_or_404(queryset: QuerySet, is_query, **kwargs):
    if is_query:
        obj = queryset.filter(**kwargs)
    else:
        obj = queryset.filter(**kwargs).first()

    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="数据不存在")

    return obj
