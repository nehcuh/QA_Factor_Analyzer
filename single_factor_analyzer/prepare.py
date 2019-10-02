#!/usr/bin/env python

"""
数据预处理
"""
from typing import List, Tuple, Union


def get_forward_returns(factor, prices, periods: Union[int, Tuple[int]] = (1, 5, 10)):
    """
    获取因子对应 periods 的远期收益率
    :param factor: MultiIndex 的 pd.DataFrame[pd.Series], 索引为 ['日期' '股票代码'], 值为 因子值
    :param prices: 实际为一个透视表，索引为 '日期', 列为 '股票列表', 值为 'close'['open']
    :param periods: 需要计算因子远期收益的 periods
    """
    if isinstance(factor, pd.Series):
        factor = pd.DataFrame(factor)  # 方便进行索引

    if isinstance(periods, int):
        periods = (periods,)

    factor_dateset = set(factor.index.get_level_values("date"))
    factor_datelist = sorted(list(factor_dateset & set(prices.index)))

    if len(factor_datelist) == 0:
        raise ValueError("错误，输入的因子数据与输入的价格透视表的时间序列不匹配，无法计算因子远期收益")

    factor_codeset = set(factor.index.get_level_values(1).tolist())
    factor_codelist = sorted(list(set(factor_codeset & set(prices.columns))))

    if len(factor_codelist) == 0:
        raise ValueError("错误，输入的因子数据与输入的价格透视表股票列表不匹配，无法计算因子远期收益")

    factor = factor.loc[(factor_datelist, factor_codelist), :]
    prices = prices[factor_codelist]  # 注意：为了计算因子收益率，价格透视表数据日期索引往往需要比因子数据更广

    forward_returns = pd.DataFrame(
        index=pd.MultiIndex.from_product(
            [factor_datelist, factor_codelist], names=["date", "code"]
        )
    )

    for period in periods:
        forward_returns[f"period_{period}"] = (
            prices.pct_change(period).shift(-period).reindex(factor_datelist).stack()
        )

    return forward_returns


def get_demean_forward_returns(
    factor_data: pd.DataFrame, grouper: Union[str, List[str]] = None
):
    """
    因子数据进行分组去均值
    :param factor_data: 所谓为 MultiIndex, 索引为 ['日期', '股票'], dataframe 的列中必须包括因子的远期收益，
    如果包括其他信息，可以包括 分组信息 (譬如 'industry')，加权信息 (譬如 'weights')
    :param grouper: 分组信息，如果没有，则默认按日期进行去均值
    """
    factor_data = factor_data.copy()

    if not grouper:
        grouper = "date"

    cols = get_forward_returns_columns(factor_data.columns)
    factor_data[cols] = factor_data.groupby(grouper, as_index=False)[
        cols.append(pd.Index(["weights"]))
    ].apply(
        lambda x: x[cols].subtract(
            np.average(x[cols], axis=0, weights=x["weights"].fillna(0.0).values), axis=1
        )
    )
    return factor_data


def get_clean_factor(
    factor: pd.DataFrame,
    forward_returns: pd.DataFrame,
    groupby: pd.Series = None,
    weights: pd.Series = None,
    binning_by_group: bool = False,
    quantiles: Union[int, List[float], Tuple[float]] = 5,
    bins: Union[int, List[float], Tuple[float]] = None,
    max_loss: float = 0.35,
    zero_aware: bool = False,
):
    """
    因子数据格式化，最后一列为因子远期收益
    """
    initial_amount = float(len(factor.index))

    factor_copy = factor.copy()


def get_clean_factor_and_forward_returns(
    factor,
    prices,
    groupby,
    weights,
    binning_by_group,
    quantiles,
    bins,
    periods,
    max_loss=0.35,
    zero_aware=False,
):
    """
    实际因子的预处理应该是独立的，方便用户更自由的调用
    """
    forward_returns = compute_forward_returns(factor, prices, periods)
