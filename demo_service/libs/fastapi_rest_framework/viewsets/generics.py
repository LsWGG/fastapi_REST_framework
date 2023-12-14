#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：generics.py
@Time    ：2022/3/8 3:32 下午
@Desc    ：常用视图，待补充
"""
from fastapi.requests import Request
from tortoise import Model

from .helper import get_object_or_404
from ..utils.response import dict_response


class GenericAPIMixin:
    # 分页
    page = 1
    page_key = "page"
    size = 10
    size_key = "size"

    # 路径参数
    lookup_field = "id"
    lookup_type = int
    pk_param = None

    # 模型类
    model: Model = None
    # 默认Schema类：用于请求校验
    schema_class = None
    # 默认响应模型：用于定义响应格式
    response_model = None

    # 权限相关：获取用户
    @staticmethod
    def get_current_user():
        return None

    current_user = get_current_user

    @classmethod
    def get_object(cls, request: Request, is_query=False):
        assert cls.pk_param is not None, (
            f"{cls.__name__} should either include a `pk_param` attribute. "
        )
        filter_kwargs = {cls.lookup_field: cls.pk_param}
        obj = get_object_or_404(cls.get_queryset(request), is_query, **filter_kwargs)
        return obj

    @classmethod
    def get_queryset(cls, request: Request):
        assert cls.model is not None, (
            f"{cls.__name__} should either include a `model` attribute. "
        )
        queryset = cls.model.all()
        return queryset

    @classmethod
    def get_schema(cls, action):
        _type = "schema_class"
        schema = cls.get_schema_class(action, _type)
        try:
            # 自动生成的Schema需实例化才可生效
            return schema()
        except Exception:
            # 自定义Schema无需实例化
            return schema

    @classmethod
    def get_response_model(cls, action):
        _type = "response_model"
        schema = cls.get_schema_class(action, _type)
        return schema

    @classmethod
    def get_schema_class(cls, action, _type):
        assert (cls.schema_class and cls.response_model), (
            f"{cls.__name__} should either include schema_class and response_model attribute. "
        )

        if hasattr(cls, action + "_" + _type):
            return getattr(cls, action + "_" + _type)
        else:
            return getattr(cls, _type)

    @classmethod
    def format_response(cls, *args, **kwargs):
        return dict_response(*args, **kwargs)
