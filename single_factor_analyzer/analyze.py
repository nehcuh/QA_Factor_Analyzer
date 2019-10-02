#!/usr/bin/env python

"""
因子分析模块
"""

from typing import Union

import numpy as np
import pandas as pd


class FactorAnalyzer:
    """
    单因子分析模块
    """

    def __init__(
        self,
        factor,
        prices,
        groupby,
        weights,
        quantiles,
        bins,
        periods,
        binning_by_group,
        max_loss,
        zero_aware,
    ):
        """
        """
        self.factor = factor
        self.prices = prices
        self.groupby = groupby

    def __gen_clean_factor_and_forward_returns(self):
        """
        因子数据格式化，获取收益
        """
        factor_data = self.factor
        if isinstance(factor_data, pd.DataFrame):
            factor_data = factor_data.stack(dropna=False)

        stocks = sorted(list(factor_data.index.get_level_values(1).drop_duplicates()))
        start_date = min(factor_data.index.get_level_values(0))
        end_date = max(factor_data.index.get_level_values(0))

        prices = self.prices
        groupby = self.groupby
        weights = self.weights

        # self._clean_factor_data = get_clean_factor_and_forward_returns(
        #     factor_data,
        #     prices,
        #     groupby=groupby,
        #     weights=weights,
        #     binning_by_group=self._binning_by_group,
        #     quantiles=self._quantiles,
        #     bins=self._bins,
        #     periods=self._periods,
        #     max_loss=self._max_loss,
        #     zero_aware=self._zero_aware,
        # )
