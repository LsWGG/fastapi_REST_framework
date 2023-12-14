#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：__init__.py
@Time    ：2023/12/6 10:55
@Desc    ：
"""
import uvicorn

from demo_service import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app', port=8080, host='0.0.0.0', reload=False, proxy_headers=False)
