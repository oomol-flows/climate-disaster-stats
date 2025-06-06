from oocana import Context
import pandas as pd
import numpy as np


def main(params: dict, context: Context):

    climate_data = params["climate_data"]

    weekly_stats = params["weekly_stats"]

    # Adjust the standard deviation range of the normal distribution evaluation criteria for January-April and October-December. The smaller the value, the more disasters.
    sigma1 = params["sigma1"]

    # Adjust the standard deviation range of the normal distribution evaluation criteria for May-September. The smaller the value, the more disasters.
    sigma2 = params["sigma2"]

    # Convert the date column to date format
    climate_data["日期"] = pd.to_datetime(climate_data["日期"], format="%Y%m%d")

    # Add a new column to represent the week number of each year
    climate_data["周"] = climate_data["日期"].dt.isocalendar().week

    # Filter out data from 2010 to 2020
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
