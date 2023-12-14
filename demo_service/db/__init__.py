# -*- coding: utf-8 -*-
from fastapi import FastAPI
from tortoise import Tortoise


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['demo_service.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


def init_db(app: FastAPI):
    """
    初始化db连接
    :param app: FastAPI
    :return:
    """

    @app.on_event("startup")
    async def init_conn():
        await init()

    @app.on_event("shutdown")
    async def close_conn():
        pass
