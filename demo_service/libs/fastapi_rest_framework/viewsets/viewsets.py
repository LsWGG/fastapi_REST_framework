#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：router.py
@Time    ：2022/3/9 9:19 上午
@Desc    ：
"""
from . import generics
from . import mixins


class GenericViewSet(generics.GenericAPIMixin):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass


class ReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `destroy()` and `list()` actions.
    """
    pass


class CreateOrUpdateModelViewSet(
    mixins.CreateOrUpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    """
    A viewset that provides default `create_or_update()`, `retrieve()`, `destroy()` and `list()` actions.
    """
    pass
