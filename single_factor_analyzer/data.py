#!/usr/bin/env python
"""
数据接口
TODO: 给 QA 增加 QA_fetch_stock_industry 接口
"""

from functools import partial
from typing import Union

import numpy as np
import pandas as pd
from fastcache import lru_cache

import QUANTAXIS as QA

from .param import WeightMethod
from .when import date2str


class DataApi:
    """
    数据接口
    """

    def __init__(
        self,
        price_type: str = "close",
        fq: str = "post",
        industry: str = "sw_l1",
        weight_method: str = "avg",
    ):
        pass

    def get_prices(
        self, code_list: Union(str, List[str]), start_date: str, end_date: str
    ):
        """
        返回价格数据，注意，这里取的是日线数据
        :param code_list: 股票池
        :param start_date: 起始时间
        :param end_date: 结束时间
        """
        if isinstance(code_list):
            code_list = [code_list]
        if self.fq in ["post", "hfq", "后复权"]:
            return (
                QA.QA_fetch_stock_day_adv(
                    code=code_list, start=start_date, end=end_date
                )
                .to_hfq()
                .pivot(price_type)
            )
        elif self.fq in ["pre", "qfq", "前复权"]:
            return (
                QA.QA_fetch_stock_day_adv(
                    code=code_list, start=start_date, end=end_date
                )
                .to_qfq()
                .pivot(price_type)
            )
        else:
            return QA.QA_fetch_stock_day_adv(
                code=code_list, start=start_date, end=end_date
            ).pivot(price_type)

    def get_groupby(
        self,
        code_list: Union(str, List[str]),
        start_date: str = None,
        end_date: str = None,
        method: str = "rough",
        industry: str = "sw_l1",
    ):
        """
        获取股票列表对应的行业列表，默认为粗糙获取模式，即用当前股票所属行业作为其历史行业
        :param code_list: 股票列表
        :param start_date: 起始时间
        :param end_date: 结束时间
        """
        if isinstance(code_list, str):
            code_list = [code_list]
        if not start_date:
            if not end_date:
                end_date = str(datetime.date.today())
            return QA.QA_fetch_stock_industry(
                code=code_list, start=end_date, end=end_date, industry=industry
            )
        if not end_date:
            end_date = str(datetime.date.today())
        return QA.QA_fetch_stock_industry(
            code=code_list, start=start_date, end=end_date, industry=industry
        )

    def get_weights(
        self,
        code_list: Union(str, List[str]),
        start_date: str,
        end_date: str,
        method: str = WeightMethod.AVG,
    ):
        """
        获取加权值
        """
        if isinstance(code_list, str):
            code_list = [code_list]
        if method is WeightMethod.AVG:
            trade_dates = QA.QA_util_get_trade_range(start_date, end_date)
            df_local = pd.DataFrame(index=trade_dates, columns=code_list).fillna(1.0)
            df_local.index = pd.to_datetime(df_local.index)
            return df_local
        market_value = QA.QAAnalysis_block(
            code=code_list, start_date=start_date, end_date=end_date
        ).market_value
        if method is WeightMethod.MKT:
            return df.reset_index().pivot(index=date, columns=code, values="mv")
        if method is WeightMethod.SQRTMKT:
            return (
                df.reset_index()
                .pivot(index=date, columns=code, values="mv")
                .transform("sqrt")
            )
        if method is WeightMethod.LNMKT:
            return (
                df.reset_index()
                .pivot(index=date, columns=code, values="mv")
                .transform("log")
            )
        if method is WeightMethod.CMKT:
            return df.reset_index().pivot(
                index=date, columns=code, values="liquidity_mv"
            )
        if method is WeightMethod.SQRTCMKT:
            return (
                df.reset_index()
                .pivot(index=date, columns=code, values="liquidity_mv")
                .transform("sqrt")
            )
        if method is WeightMethod.LNCMKT:
            return (
                df.reset_index()
                .pivot(index=date, columns=code, values="liquidity_mv")
                .transform("log")
            )
        else:
            raise ValueError("{} 加权方式未实现".format(method))

    @property
    def apis(self):
        return dict(
            prices=self.get_prices, groupby=self.get_groupby, weights=self.get_weights
        )
