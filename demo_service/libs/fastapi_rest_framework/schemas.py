#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：schemas_pro.py
@Time    ：2022/3/8 10:13 上午
@Desc    ：
"""
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

                if hasattr(cls, "PydanticMeta"):
                    model_class.PydanticMeta = getattr(cls, "PydanticMeta")

                fields = {
                    "name": cls.__name__
                }
                if hasattr(meta_class, "is_many"):
                    return cls.many_init(model_class, **fields)
                else:
                    schema = cls.single_init(model_class, **fields)
                schema.Config = getattr(cls, "Config")
                return schema

        else:
            return super().__new__(cls)

    @classmethod
    def model_init(cls):
        if hasattr(cls, 'get_models_paths'):
            return Tortoise.init_models(cls.get_models_paths(), "models")
        else:
            return Tortoise.init_models(["__main__"], "models")

    @classmethod
    def many_init(cls, model_class, **kwargs):
        return pydantic_queryset_creator(model_class, **kwargs)

    @classmethod
    def single_init(cls, model_class, **kwargs):
        # config_class中fields配置不生效，pydantic_model_creator不支持
        return pydantic_model_creator(model_class, model_config=cls.Config.__dict__, **kwargs)

    class Config:
        error_msg_templates = ERROR_MSG_TEMPLATE
