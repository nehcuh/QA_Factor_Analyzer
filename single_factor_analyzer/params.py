#!/usr/bin/env python

"""
常量定义
"""


class WeightMethod:
    """
    加权方式
    """

    AVG = "avg"  # 等权重
    MKT = "mktcap"  # 市值加权
    SQRTMKT = "sqtmktcap"  # 市值平方根加权
    LNMKT = "lnmktcap"  # 市值对数加权
    CMKT = "cmktcap"  # 流通市值加权
    SQRTCMKT = "sqrtcmktcap"  # 流通市值平方根加权
    LNCMKT = "lncmktcap"  # 对数流通市值加权
