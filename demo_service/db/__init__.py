# -*- coding: utf-8 -*-
from fastapi import FastAPI
from loguru import logger
from tortoise import Tortoise


async def db_init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    logger.info("初始化数据库连接...")
    await Tortoise.init(
        # PG
        db_url='postgres://postgres:postgres@192.168.1.203:5422/diplomacy',

        # SQLite
        # db_url='sqlite://db.sqlite3',
        modules={'models': ['demo_service.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


async def db_clone():
    logger.info("关闭数据库连接...")
    await Tortoise.close_connections()


def init_db(app: FastAPI):
    """
    初始化db连接
    :param app: FastAPI
    :return:
    """

    @app.on_event("startup")
    async def init_conn():
        await db_init()

    @app.on_event("shutdown")
    async def close_conn():
        await db_clone()
