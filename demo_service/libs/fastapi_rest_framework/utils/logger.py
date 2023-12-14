#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：logger.py
@Time    ：2022/7/12 14:36
@Desc    ：日志模块
"""
import logging
import os
import sys

from loguru import logger


def get_logger(log_name):
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    log_path = os.path.abspath(os.path.dirname(os.getcwd()))
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    log_path = os.path.join(log_path, log_name + ".log")
    kwargs = {
        "sink": log_path,
        "compression": "zip",
        "rotation": "00:00",
        "backtrace": True,
        "diagnose": True,
        "retention": "5 days",
        "enqueue": True,
        "level": "DEBUG",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {file} | {name}:{module}:{line} {message}"
    }
    # log文件
    logger.add(**kwargs)
    logger.configure(handlers=[
        kwargs,
        {"sink": sys.stderr, "backtrace": False, "diagnose": False}
    ])
    return logger
