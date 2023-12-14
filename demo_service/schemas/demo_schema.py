#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：demo_schema.py
@Time    ：2023/12/14 15:08
@Desc    ：
"""
from typing import Union

from pydantic import BaseModel

from demo_service.models import Tournament
from demo_service.schemas import GenericSerializerSchemas, BaseResponseMode, BaseResponseListSchema


class TournamentSchema(GenericSerializerSchemas):
    class Meta:
        model = Tournament


class CreateOrUpdateTournamentSchema(TournamentSchema):
    class PydanticMeta:
        exclude = ("id",)


class ListTournamentSchema(TournamentSchema):
    class Meta:
        is_many = True
        model = Tournament


class ResponseTournamentSchema(BaseResponseMode):
    data: Union[None, TournamentSchema()]


class ResponseListTournamentSchema(BaseResponseListSchema):
    class ListData(BaseModel):
        data: Union[None, ListTournamentSchema()]
        count: int

    data: ListData
