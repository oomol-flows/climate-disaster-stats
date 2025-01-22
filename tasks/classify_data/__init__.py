from oocana import Context
import pandas as pd
import numpy as np


def main(params: dict, context: Context):

    climate_data = params["climate_data"]

    weekly_stats = params["weekly_stats"]

    # 调整1-4月，10-12月正态分布评估标准的标准差范围，数值越小，灾害越多
    sigma1 = params["sigma1"]

    # 调整5-9月正态分布评估标准的标准差范围，数值越小，灾害越多
    sigma2 = params["sigma2"]

    # 将日期列转换为日期格式
    climate_data["日期"] = pd.to_datetime(climate_data["日期"], format="%Y%m%d")

    # 添加一个新的列来表示每年的周数
    climate_data["周"] = climate_data["日期"].dt.isocalendar().week

    # 筛选出2010年至2020年的数据
    data = climate_data[
        (climate_data["日期"].dt.year >= params["year_from"])
        & (climate_data["日期"].dt.year <= params["year_to"])
    ]

    data["分类"] = np.select(
        [
            (
                (
                    data["周"].map(weekly_stats["mean"])
                    + sigma1 * data["周"].map(weekly_stats["std"])
                )
                < data[params["indicator"]]
            )
            & (
                ((data["日期"].dt.month >= 1) & (data["日期"].dt.month <= 4))
                | ((data["日期"].dt.month >= 10) & (data["日期"].dt.month <= 12))
            ),
            (
                (
                    data["周"].map(weekly_stats["mean"])
                    + sigma2 * data["周"].map(weekly_stats["std"])
                )
                < data[params["indicator"]]
            )
            & ((data["日期"].dt.month >= 5) & (data["日期"].dt.month <= 9)),
            (
                (
                    data["周"].map(weekly_stats["mean"])
                    - sigma1 * data["周"].map(weekly_stats["std"])
                )
                > data[params["indicator"]]
            )
            & (
                ((data["日期"].dt.month >= 1) & (data["日期"].dt.month <= 4))
                | ((data["日期"].dt.month >= 10) & (data["日期"].dt.month <= 12))
            ),
            (
                (
                    data["周"].map(weekly_stats["mean"])
                    - sigma2 * data["周"].map(weekly_stats["std"])
                )
                > data[params["indicator"]]
            )
            & ((data["日期"].dt.month >= 5) & (data["日期"].dt.month <= 9)),
        ],
        params["levels"],
        default="正常",
    )

    data["日期"] = pd.to_datetime(data["日期"], format="%Y%m%d")
    data["周"] = data["日期"].dt.isocalendar().week
    data["月"] = data["日期"].dt.month
    data["年"] = data["日期"].dt.year
    data["周"] = data.groupby(["月"])["周"].transform(lambda x: pd.factorize(x)[0] + 1)

    return {"disaster": data}
