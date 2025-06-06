from oocana import Context
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set matplotlib font to prevent Chinese garbled characters
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Source Han Sans SC"]

def main(params: dict, context: Context):
    # Get rice yield data
    yieldData = params["yield_data"]
    # Group by region
    grouped = yieldData.groupby("name")

    # Get data for different disaster types
    df1 = params["tmp_disaster"]
    df2 = params["precipitation_disaster"]
    df3 = params["wind_disaster"]
    df4 = params["humidity_disaster"]

    image_paths = []
    # Directory for output images
    output_dir = context.session_dir

    # Generate and save charts for each region
    for name, group in grouped:
        # Process precipitation disaster data
        disasterTmp = df1[df1["市"] == name]
        disasterTmp = disasterTmp[["周", "分类", "月", "日期"]]
        # Calculate the month of disaster occurrence (week as decimal)
        disasterTmp["num"] = (disasterTmp["周"] - 1) / 4 + (disasterTmp["月"] - 1)
        disasterTmp["年"] = pd.to_datetime(disasterTmp["日期"]).dt.year
        # Keep only records for heavy and light precipitation
        disasterTmp = disasterTmp[disasterTmp["分类"].isin(["降水多", "降水少"])]

        # Process temperature disaster data
        disasterTmp2 = df2[df2["市"] == name]
        disasterTmp2 = disasterTmp2[["周", "分类", "月", "日期"]]
        disasterTmp2["num"] = (disasterTmp2["周"] - 1) / 4 + (disasterTmp2["月"] - 1)
        disasterTmp2["年"] = pd.to_datetime(disasterTmp2["日期"]).dt.year
        # Keep only records for high and low temperatures
        disasterTmp2 = disasterTmp2[disasterTmp2["分类"].isin(["高温", "低温"])]

        # Process wind disaster data
        disasterTmp3 = df3[df3["市"] == name]
        disasterTmp3 = disasterTmp3[["周", "分类", "月", "日期"]]
        disasterTmp3["num"] = (disasterTmp3["周"] - 1) / 4 + (disasterTmp3["月"] - 1)
        disasterTmp3["年"] = pd.to_datetime(disasterTmp3["日期"]).dt.year
        # Keep only records for high and low wind speeds
        disasterTmp3 = disasterTmp3[disasterTmp3["分类"].isin(["风速大", "风速小"])]

        # Process humidity disaster data
        disasterTmp4 = df4[df4["市"] == name]
        disasterTmp4 = disasterTmp4[["周", "分类", "月", "日期"]]
        disasterTmp4["年"] = pd.to_datetime(disasterTmp4["日期"]).dt.year
        disasterTmp4["num"] = (disasterTmp4["周"] - 1) / 4 + (disasterTmp4["月"] - 1)
        # Keep only records for humid and dry conditions
        disasterTmp4 = disasterTmp4[disasterTmp4["分类"].isin(["湿润", "干旱"])]

        # Create chart and twin y-axes
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        # Plot bar chart of rice yield per unit area over the years
        ax1.bar(
            list(group["year"]),
            list(group["yieldPerArea"]),
            label=name,
            alpha=0.3,
        )
        ax1.set_xlabel("年份")
        ax1.set_ylabel("水稻单位面积产量")

        # Plot heavy precipitation disaster points
        high_temp = disasterTmp[disasterTmp["分类"] == "降水多"]
        ax2.plot(
            high_temp["年"],
            high_temp["num"],
            "s",
            color="b",
            label="降水多",
            markersize=3,
        )
        ax2.set_ylabel("月份")

        # Plot light precipitation disaster points
        low_temp = disasterTmp[disasterTmp["分类"] == "降水少"]
        ax2.plot(
            low_temp["年"],
            low_temp["num"],
            "s",
            color="cornflowerblue",
            label="降水少",
            markersize=3,
        )

        # Plot high temperature disaster points
        high_temp2 = disasterTmp2[disasterTmp2["分类"] == "高温"]
        ax2.plot(
            high_temp2["年"],
            high_temp2["num"],
            "o",
            color="darkred",
            label="高温",
            markersize=3,
        )

        # Plot low temperature disaster points
        low_temp2 = disasterTmp2[disasterTmp2["分类"] == "低温"]
        ax2.plot(
            low_temp2["年"],
            low_temp2["num"],
            "o",
            color="lightcoral",
            label="低温",
            markersize=3,
        )

        # Plot high wind speed disaster points
        low_temp3 = disasterTmp3[disasterTmp3["分类"] == "风速大"]
        ax2.plot(
            low_temp3["年"],
            low_temp3["num"],
            "^",
            color="#696969",
            label="风速大",
            markersize=3,
        )

        # Plot dry disaster points
        low_temp4 = disasterTmp4[disasterTmp4["分类"] == "干旱"]
        ax2.plot(
            low_temp4["年"],
            low_temp4["num"],
            "^",
            color="#E89F12",
            label="干旱",
            markersize=3,
        )
        # Set y-axis range
        ax2.set_ylim(0, 12)

        # Set chart title
        plt.title(f"灾害对{name}水稻单位面积产量的影响分析")
        plt.legend()

        # Save chart to file
        image_path = os.path.join(output_dir, f"{name}_plot.png")
        plt.savefig(image_path, dpi=300)
        plt.close(fig)
        image_paths.append(image_path)

    # Preview generated images
    context.preview(
        {
            "type": "image",
            "data": image_paths,
        }
    )
    # Return image paths
    return {"charts": image_paths}