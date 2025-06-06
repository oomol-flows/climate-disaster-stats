from oocana import Context
import pandas as pd

def main(params: dict, context: Context):

    data = params["climate_data"]

    # Convert date column to datetime format
    data["日期"] = pd.to_datetime(data["日期"], format="%Y%m%d")

    # Add a new column to represent the week number of each year
    data["周"] = data["日期"].dt.isocalendar().week

    # Filter out data from 2001 to 2009
    data = data[
        (data["日期"].dt.year >= params["year_from"])
        & (data["日期"].dt.year <= params["year_to"])
    ]

    # Group by week and calculate mean and standard deviation for each week
    weekly_stats = data.groupby("周")[params["indicator"]].agg(["mean", "std"])

    return {"stats": weekly_stats}
