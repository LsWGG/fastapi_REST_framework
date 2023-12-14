#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：mixins.py
@Time    ：2022/3/8 3:22 下午
@Desc    ：通用操作Mixin类，因FastAPI通过参数形式校验传值，故需使用MakeMixin提供方法初始化函数
"""
from . import generics

from .dynamic_methods import MakeMixin
from .helper import is_method_overloaded


class CreateModelMixin:
    """
    Create a model instance.
    """

    def __init_subclass__(cls: generics.GenericAPIMixin, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_method_overloaded(cls, 'create') and cls.model:
            cls.create = classmethod(
                MakeMixin.make_create(
                    schema_class=cls.get_schema('create'),
                    get_current_user=cls.current_user
                )
            )


class ListModelMixin:
    """
    List a queryset.
    """

    def __init_subclass__(cls: generics.GenericAPIMixin, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_method_overloaded(cls, 'list') and cls.model:
            cls.list = classmethod(
                MakeMixin.make_list(
                    cls.page,
                    cls.page_key,
                    cls.size,
                    cls.size_key,
                    schema_class=cls.get_schema('list'),
                    get_current_user=cls.current_user,
                    **kwargs
                ),
            )


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def __init_subclass__(cls: generics.GenericAPIMixin, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_method_overloaded(cls, 'retrieve') and cls.model:
            cls.retrieve = classmethod(
                MakeMixin.make_retrieve(
                    cls.lookup_field,
                    cls.lookup_type,
                    schema_class=cls.get_schema('retrieve'),
                    get_current_user=cls.current_user,
                    **kwargs
                ),
            )


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def __init_subclass__(cls: generics.GenericAPIMixin, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_method_overloaded(cls, 'update') and cls.model:
            cls.update = classmethod(
                MakeMixin.make_update(
                    cls.lookup_field,
                    cls.lookup_type,
                    schema_class=cls.get_schema('update'),
                    get_current_user=cls.current_user
                )
            )


class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def __init_subclass__(cls: generics.GenericAPIMixin, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_method_overloaded(cls, 'destroy') and cls.model:
            cls.destroy = classmethod(
                MakeMixin.make_destroy(
                    cls.lookup_field,
                    cls.lookup_type,
                    schema_class=cls.get_schema('destroy'),
                    get_current_user=cls.current_user
                )
            )
