#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：dynamic_methods.py
@Time    ：2022/3/10 10:03 上午
@Desc    ：为Mixin提供具体的逻辑操作
"""
from fastapi import HTTPException, Path, Query, Request, Body, status, Security
from tortoise.contrib.pydantic import PydanticModel


class MakeMixin:
    @classmethod
    def make_list(cls, _page, page_key, _size, size_key, schema_class: PydanticModel, **kwargs):
        async def list(
                self,
                request: Request,
                user=Security(kwargs.get("get_current_user")),
                page: int = Query(_page, alias=page_key),
                limit: int = Query(_size, alias=size_key),
        ):
            skip = (page - 1) * limit
            # from_queryset 作用是获取关联数据
            try:
                data = await schema_class.from_queryset(
                    self.get_queryset(request=request).offset(skip).limit(limit).all()
                )
                res = {
                    "data": data,
                    "count": await self.get_queryset(request=request).count()
                }
                return self.format_response(res)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

        return list

    @classmethod
    def make_retrieve(cls, lookup_field, lookup_type, schema_class: PydanticModel, **kwargs):
        async def retrieve(
                self,
                request: Request,
                user=Security(kwargs.get("get_current_user")),
                param: lookup_type = Path(..., alias=lookup_field)
        ):
            self.pk_param = param
            res = await self.get_object(request)
            if not res:
                return self.format_response(data=None, message="数据不存在或已删除")
                # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="数据不存在")

            try:
                data = await schema_class.from_tortoise_orm(res)
                return self.format_response(data)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

        return retrieve

    @classmethod
    def make_create(cls, schema_class: PydanticModel, **kwargs):
        async def create(
                self,
                request: Request,
                user=Security(kwargs.get("get_current_user")),
                validated_data: schema_class = Body(...)
        ):
            try:
                data = await self.model.create(**validated_data.dict())
                return self.format_response(data)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

        return create

    @classmethod
    def make_update(cls, lookup_field, lookup_type, schema_class: PydanticModel, **kwargs):
        async def update(
                self,
                request: Request,
                user=Security(kwargs.get("get_current_user")),
                validated_data: schema_class = Body(...),
                param: lookup_type = Path(..., alias=lookup_field),
        ):
            self.pk_param = param
            res = await self.get_object(request)
            if not res:
                return self.format_response(data=None, message="数据不存在或已删除")
                # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="数据不存在")

            try:
                await self.get_object(request).update(**validated_data.dict())
                data = await self.get_object(request)
                return self.format_response(data)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

        return update

    @classmethod
    def make_destroy(cls, lookup_field, lookup_type, schema_class: PydanticModel, **kwargs):
        async def destroy(
                self,
                request: Request,
                user=Security(kwargs.get("get_current_user")),
                param: lookup_type = Path(..., alias=lookup_field),
        ):
            self.pk_param = param
            try:
                await self.get_object(request).delete()
                return self.format_response("删除成功")
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

        return destroy
