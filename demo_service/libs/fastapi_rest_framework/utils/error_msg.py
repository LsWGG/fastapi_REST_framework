#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：error_msg.py
@Time    ：2022/9/8 16:01
@Desc    ：自定义响应格式
"""
# key值详见，pydantic源码 /pydantic/pydantic/errors.py

# todo: 若不满足可自行添加
ERROR_MSG_TEMPLATE = {
    # base
    "value_error.missing": "该字段为必填项",
    "type_error.none.not_allowed": "数据不存在",
    # str
    "value_error.any_str.max_length": "最大长度为: {limit_value}",
    "value_error.any_str.min_length": "最小长度为: {limit_value}",
    "value_error.str.regex": "字符串与正则表达不匹配: {pattern}",
    # int
    "value_error.number.not_gt": "字段应大于: {limit_value}",
    "value_error.number.not_ge": "字段应大于或等于: {limit_value}",
    "value_error.number.not_lt": "字段应小于: {limit_value}",
    "value_error.number.not_le": "字段应小于或等于: {limit_value}",
    # float
    "value_error.decimal": "该字段应为float类型",
    "value_error.decimal.not_finite": "该字段应为float类型",
    "value_error.decimal.max_digits": "总位数最大为: {max_digits}",
    "value_error.decimal.max_places": "小数位数最大为: {decimal_places}",
    "value_error.decimal.whole_digits": "整数位最大为: {whole_digits}",
    # bool
    "value_error.bool": "无法将值解析为布尔值",
    # datetime
    # time
    # uuid
}
