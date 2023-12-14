#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：response.py
@Time    ：2022/3/24 9:58 上午
@Desc    ：统一返回格式
"""
from fastapi import status
from fastapi.responses import JSONResponse, Response


def response(data=None, message="成功", status_code=status.HTTP_200_OK, code=2000) -> Response:
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code,
            "message": message,
            "data": data
        }
    )


def dict_response(data=None, message="成功", code=2000) -> dict:
    return {
        "code": code,
        "message": message,
        "data": data
    }
