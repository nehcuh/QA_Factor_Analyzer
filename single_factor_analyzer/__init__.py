#!/usr/bin/env python
from typing import Union

from .data import DataApi
from .version import __version


def analyze_factor(
    factor: pd.DataFrame,
    industry: str = "sw_l1",
    quantiles: int = 5,
    periods: Union(int, tuple) = (1, 5, 10),
    weight_method: str = "avg",
    max_loss: float = 0.25,
):
    """
    单因子分析模块

    :param factor: 因子值，columns 为股票代码， index 为日期
    :param industry: 行业分类，默认支持 "jq_l1"/"jq_l2"/"sw_l1"/"sw_l2"/"sw_l3"/"zjh"
    :param quantiles: 分位数数量，默认为 5
    :param periods: 调仓周期
    :param weight_method: 计算分位收益时，加权方法，支持 "avg"/"mktcap"/"ln_mktcap"/"cmktcap"/"ln_cmktcap"
    :param max_loss: 因重复值或 nan 值太多而无效的因子值最大占比，默认为 0.25
    """
    dataapi = DataApi(industry=industry, weight_method=weight_method)  # 数据接口
    return FactorAnalyzer(
        factor, quantiles=quantiles, periods=periods, max_loss=max_loss, **dataapi.apis
    )
