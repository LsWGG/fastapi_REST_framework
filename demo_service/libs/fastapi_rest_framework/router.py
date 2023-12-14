#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：router.py
@Time    ：2022/3/9 4:18 下午
@Desc    ：自动注册路由并绑定Schema
"""
from fastapi import APIRouter


class MainRouter(APIRouter):
    __doc__ = """
        自动注册增删改查路由
    """

    @classmethod
    def _build_single_obj_path(cls, base_path, lookup_field, lookup_type):
        return f'{base_path}/{{{lookup_field}:{lookup_type.__name__}}}'

    def is_view(self, view, base_path: str = '', **kwargs):
        assert hasattr(view, 'get_schema'), (
            f"{view.__name__} should either include a `get_schema` attribute, or override the `get_schema()` method."
        )
        tags = kwargs.get("tags") or self.tags
        lookup_field = getattr(view, 'lookup_field', 'pk')
        lookup_type = getattr(view, 'lookup_type', int)

        pk_path = self._build_single_obj_path(base_path, lookup_field, lookup_type)

        if hasattr(view, 'create'):
            method = self.post(
                path=base_path,
                response_model=getattr(view, 'get_response_model')("create"),
                tags=tags,
                name=tags[0] + " >> POST Create" if tags else "POST Create",
                **kwargs
            )
            method(view.create)

        if hasattr(view, 'list'):
            # print(getattr(view, 'get_response_model')("list").schema_json(indent=4))
            method = self.get(
                path=base_path,
                response_model=getattr(view, 'get_response_model')("list"),
                tags=tags,
                name=tags[0] + " >> Get List" if tags else "Get List",
                **kwargs
            )
            method(view.list)

        if hasattr(view, 'retrieve'):
            # print(getattr(view, 'get_schema')("retrieve").schema_json(indent=4))
            method = self.get(
                path=pk_path,
                response_model=getattr(view, 'get_response_model')("retrieve"),
                tags=tags,
                name=tags[0] + " >> Get Retrieve" if tags else "Get Retrieve",
                **kwargs
            )
            method(view.retrieve)

        if hasattr(view, 'update'):
            method = self.put(
                path=pk_path,
                response_model=getattr(view, 'get_response_model')("update"),
                tags=tags,
                name=tags[0] + " >> PUT Update" if tags else "PUT Update",
                **kwargs
            )
            method(view.update)

        if hasattr(view, 'destroy'):
            method = self.delete(
                path=pk_path,
                # response_model=getattr(view, 'get_response_model')("destroy"),
                tags=tags,
                name=tags[0] + " >> DELETE Destroy" if tags else "DELETE Destroy",
                **kwargs
            )
            method(view.destroy)
        return self
