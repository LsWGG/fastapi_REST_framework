#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：api.py
@Time    ：2023/12/6 10:54
@Desc    ：
"""
from ..libs.fastapi_rest_framework.viewsets import ModelViewSet
from ..models import Tournament
from ..schemas.demo_schema import (
    TournamentSchema,
    ResponseTournamentSchema,
    CreateOrUpdateTournamentSchema,
    ResponseListTournamentSchema,
)


class TournamentViewSet(ModelViewSet):
    """
    赛事增删改查
    """
    # 数据库模型类
    model = Tournament

    # Schema类：请求参数校验
    schema_class = TournamentSchema
    create_schema_class = CreateOrUpdateTournamentSchema
    update_schema_class = CreateOrUpdateTournamentSchema

    # 响应模型：定义响应格式
    response_model = ResponseTournamentSchema
    list_response_model = ResponseListTournamentSchema
