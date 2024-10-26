#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：dynamic_methods.py
@Time    ：2022/3/10 10:03 上午
@Desc    ：为Mixin提供具体的逻辑操作
"""
import traceback
from loguru import logger

from tortoise.contrib.pydantic import PydanticModel
from tortoise.transactions import in_transaction
from fastapi import Path, Query, Request, Body, status, Security

from .helper import get_model, get_foreign_key


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
                logger.info(f"FRF List: page:{page}; limit:{limit}; skip:{skip}")
                data = await schema_class.from_queryset(
                    self.get_queryset(request=request).offset(skip).limit(limit).all()
                )
                res = {
                    "data": data,
                    "count": await self.get_queryset(request=request).count()
                }
                return self.format_response(res)
            except Exception as e:
                logger.error(traceback.format_exc())
                return self.format_response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))

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

            try:
                logger.info(f"FRF Retrieve: {param}")
                data = await schema_class.from_tortoise_orm(res)
                return self.format_response(data)
            except Exception as e:
                logger.error(traceback.format_exc())
                return self.format_response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))

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
                logger.info(f"FRF Create: {self.model} < {validated_data}")

                async with in_transaction("default"):
                    base_data, relation_data = self.format_validated_data(validated_data)

                    # 主数据
                    data = await self.model.create(**base_data)
                    # 关联数据
                    if relation_data:
                        logger.info(f"FRF Create Relation: {relation_data}")
                        for key, value in relation_data.items():
                            rel_model_name, backward_name = key.split("__")
                            rel_model = get_model(rel_model_name)
                            rel_foreign_key = get_foreign_key(rel_model, backward_name=backward_name)

                            for rel_data in value:
                                rel_data[rel_foreign_key] = data.id
                                await rel_model.create(**rel_data)

                logger.info(f"FRF Create End: {data}")
                return self.format_response()
            except Exception as e:
                logger.error(traceback.format_exc())
                return self.format_response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))

        return create

    @classmethod
    def make_create_or_update(cls, schema_class: PydanticModel, **kwargs):
        async def create_or_update(
                self,
                request: Request,
                user=Security(kwargs.get("get_current_user")),
                validated_data: schema_class = Body(...)
        ):
            try:
                logger.info(f"FRF Create Or Update: {self.model} < {validated_data}")

                async with in_transaction("default"):
                    for data in validated_data.__root__:
                        update_data = data.dict()
                        pk = update_data.pop("id", None)
                        instance, created = await self.model.update_or_create(defaults=update_data, id=pk)
                        # if data.id:
                        #     logger.info(f"FRF Update: {data}")
                        #     updata_data = data.dict()
                        #     updata_data.pop("id")
                        #     await self.model.filter(id=data.id).first().update(**updata_data)
                        # else:
                        #     logger.info(f"FRF Create: {data}")
                        #     await self.model.create(**data.dict())

                    logger.info(f"FRF Create Or Update End {instance} > {created}")
                return self.format_response()
            except Exception as e:
                logger.error(traceback.format_exc())
                return self.format_response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))

        return create_or_update

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
                logger.info(f"FRF Update: {param} > {validated_data}")
                async with in_transaction("default"):
                    base_data, relation_data = self.format_validated_data(validated_data)

                    # 主数据
                    await self.model.update_or_create(defaults=base_data, **{lookup_field: param})
                    # 关联数据
                    if relation_data:
                        logger.info(f"FRF Update Relation: {relation_data}")
                        for key, value in relation_data.items():
                            rel_model_name, backward_name = key.split("__")
                            rel_model = get_model(rel_model_name)
                            rel_foreign_key = get_foreign_key(rel_model, backward_name=backward_name)
                            for rel_data in value:
                                rel_id = rel_data.pop(lookup_field, None)
                                await rel_model.update_or_create(
                                    defaults=rel_data, **{lookup_field: rel_id, rel_foreign_key: param}
                                )

                logger.info(f"FRF Update End...")
                return self.format_response()
            except Exception as e:
                logger.error(traceback.format_exc())
                return self.format_response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))

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
                res = await self.get_object(request)
                if not res:
                    return self.format_response(data=None, message="数据不存在或已删除")

                logger.info(f"FRF Destroy: {param} + {request.query_params}")

                await self.model.filter(**{**{lookup_field: param}, **request.query_params}).delete()
                return self.format_response()
            except Exception as e:
                logger.error(traceback.format_exc())
                return self.format_response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))

        return destroy
