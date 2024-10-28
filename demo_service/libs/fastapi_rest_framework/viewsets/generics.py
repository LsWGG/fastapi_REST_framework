#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：generics.py
@Time    ：2022/3/8 3:32 下午
@Desc    ：常用视图
"""
from tortoise import Model
from fastapi.requests import Request
from starlette.datastructures import QueryParams

from .helper import get_object_or_404, get_backward_rel_keys, get_model_name
from ..utils.generice_schema import GenericSchema
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
    # Schema生成类
    generic_schema = None

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
        if not cls.schema_class and not cls.response_model:
            gen_schema_obj = GenericSchema(cls.model)
            gen_schema_obj.init_schema(cls)

        if hasattr(cls, action + "_" + _type):
            return getattr(cls, action + "_" + _type)
        else:
            return getattr(cls, _type)

    @classmethod
    def format_response(cls, *args, **kwargs):
        return dict_response(*args, **kwargs)

    @classmethod
    def filter_model_files(cls, query_params: QueryParams):
        filters = {}
        for param in query_params:
            if param in cls.model._meta.fields:
                filters[param] = query_params[param]
            if "__" in param:
                filters[param] = query_params[param]

        return filters

    @classmethod
    def format_validated_data(cls, validated_data):
        """
        格式化请求字段，返回主数据和关联数据
        """
        relation_data = {}
        relation_keys = get_backward_rel_keys(cls.model)
        if relation_keys:
            validated_data_dict = validated_data.dict()
            for key in relation_keys:
                if not hasattr(validated_data, key):
                    continue

                rel_data = getattr(validated_data, key)
                if not rel_data:
                    validated_data_dict.pop(key)
                    continue
                relation_data.setdefault(f"{get_model_name(cls.model, key)}__{key}", []).extend(
                    validated_data_dict.pop(key)
                )
        else:
            validated_data_dict = validated_data.dict()

        return validated_data_dict, relation_data
