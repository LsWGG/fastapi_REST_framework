#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：schemas_pro.py
@Time    ：2022/3/8 10:13 上午
@Desc    ：
"""
from typing import Union

from tortoise import Tortoise
from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator, pydantic_queryset_creator

from .utils.error_msg import ERROR_MSG_TEMPLATE


class BaseSerializerSchemas(PydanticModel):

    def __new__(cls, *args, **kwargs):
        cls.model_init()

        # 根据模型类自动生成pedantic模型
        if hasattr(cls, "Meta"):
            meta_class = getattr(cls, "Meta")
            if hasattr(meta_class, "model"):
                model_class = getattr(meta_class, "model")
                fields = dict(name=cls.__name__)
                if hasattr(cls, "PydanticMeta"):
                    model_class.PydanticMeta = getattr(cls, "PydanticMeta")
                    for k, v in model_class.PydanticMeta.__dict__.items():
                        if not k.startswith("__"):
                            fields[k] = v

                if hasattr(meta_class, "is_many"):
                    return cls.many_init(model_class, **fields)
                else:
                    schema = cls.single_init(model_class, **fields)
                    return schema

        else:
            return super().__new__(cls)

    @classmethod
    def get_models_paths(cls):
        return ["__main__"]

    @classmethod
    def model_init(cls):
        return Tortoise.init_models(cls.get_models_paths(), "models")

    @classmethod
    def many_init(cls, model_class, **kwargs):
        return pydantic_queryset_creator(model_class, **kwargs)

    @classmethod
    def single_init(cls, model_class, **kwargs):
        # config_class中fields配置不生效，pydantic_model_creator不支持
        return pydantic_model_creator(model_class, model_config=cls.Config.__dict__, **kwargs)

    class Config:
        pass
        # error_msg_templates = ERROR_MSG_TEMPLATE


class BaseResponseMode(PydanticModel):
    __doc__ = "基础响应模型类"

    data: Union[str, dict, None]
    message: Union[str, dict, None]
    code: int


class BaseResponseListSchema(PydanticModel):
    class ListData(PydanticModel):
        data: Union[str, dict, None]
        count: int

    data: ListData
