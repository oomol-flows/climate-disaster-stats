from oocana import Context
import pandas as pd

def main(params: dict, context: Context):

    data = params["climate_data"]

    # 将日期列转换为日期格式
    data["日期"] = pd.to_datetime(data["日期"], format="%Y%m%d")

    # 添加一个新的列来表示每年的周数
    data["周"] = data["日期"].dt.isocalendar().week

    # 筛选出2001年至2009年的数据
    data = data[
        (data["日期"].dt.year >= params["year_from"])
        & (data["日期"].dt.year <= params["year_to"])
    ]

    # 按周分组，计算每周的均值和标准差
    weekly_stats = data.groupby("周")[params["indicator"]].agg(["mean", "std"])

    return {"stats": weekly_stats}
