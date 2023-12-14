#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：user_model.py
@Time    ：2023/12/6 18:06
@Desc    ：
"""
from tortoise import fields
from tortoise.models import Model


class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    class Meta:
        table = "tb_tournament"
        table_description = "赛事表"

    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    tournament = fields.ForeignKeyField('models.Tournament', related_name='events')
    participants = fields.ManyToManyField('models.Team', related_name='events', through='event_team')

    class Meta:
        table = "tb_event"
        table_description = "事件表"

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    class Meta:
        table = "tb_team"
        table_description = "组队信息表"

    def __str__(self):
        return self.name
