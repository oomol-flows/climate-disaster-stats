from oocana import Context
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64
import numpy as np

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Source Han Sans SC"]


def main(params: dict, context: Context):

    yieldData = params["yield_data"]

    grouped = yieldData.groupby("name")

    df1 = params["tmp_disaster"]
    df2 = params["precipitation_disaster"]
    df3 = params["wind_disaster"]
    df4 = params["humidity_disaster"]

    images = []
    # Generate and save the plots for each area
    for name, group in grouped:

        disasterTmp = df1[df1["市"] == name]

        disasterTmp = disasterTmp[["周", "分类", "月", "日期"]]

        disasterTmp["num"] = (disasterTmp["周"] - 1) / 4 + (disasterTmp["月"] - 1)

        disasterTmp["年"] = pd.to_datetime(disasterTmp["日期"]).dt.year

        disasterTmp = disasterTmp[disasterTmp["分类"].isin(["降水多", "降水少"])]

        disasterTmp2 = df2[df2["市"] == name]

        disasterTmp2 = disasterTmp2[["周", "分类", "月", "日期"]]

        disasterTmp2["num"] = (disasterTmp2["周"] - 1) / 4 + (disasterTmp2["月"] - 1)

        disasterTmp2["年"] = pd.to_datetime(disasterTmp2["日期"]).dt.year

        disasterTmp2 = disasterTmp2[disasterTmp2["分类"].isin(["高温", "低温"])]

        disasterTmp3 = df3[df3["市"] == name]

        disasterTmp3 = disasterTmp3[["周", "分类", "月", "日期"]]

        disasterTmp3["num"] = (disasterTmp3["周"] - 1) / 4 + (disasterTmp3["月"] - 1)
        disasterTmp3["年"] = pd.to_datetime(disasterTmp3["日期"]).dt.year
        disasterTmp3 = disasterTmp3[disasterTmp3["分类"].isin(["风速大", "风速小"])]

        disasterTmp4 = df4[df4["市"] == name]

        disasterTmp4 = disasterTmp4[["周", "分类", "月", "日期"]]

        disasterTmp4["年"] = pd.to_datetime(disasterTmp4["日期"]).dt.year
        disasterTmp4["num"] = (disasterTmp4["周"] - 1) / 4 + (disasterTmp4["月"] - 1)
        disasterTmp4 = disasterTmp4[disasterTmp4["分类"].isin(["湿润", "干旱"])]

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        # # Plot yieldPerArea vs year
        ax1.bar(
            list(group["year"]),
            list(group["yieldPerArea"]),
            label=name,
            color="black",
            alpha=0.3,
        )
        ax1.set_xlabel("年份")
        ax1.set_ylabel("水稻单位面积产量")

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

        low_temp = disasterTmp[disasterTmp["分类"] == "降水少"]
        ax2.plot(
            low_temp["年"],
            low_temp["num"],
            "s",
            color="cornflowerblue",
            label="降水少",
            markersize=3,
        )

        high_temp2 = disasterTmp2[disasterTmp2["分类"] == "高温"]
        ax2.plot(
            high_temp2["年"],
            high_temp2["num"],
            "o",
            color="darkred",
            label="高温",
            markersize=3,
        )

        low_temp2 = disasterTmp2[disasterTmp2["分类"] == "低温"]
        ax2.plot(
            low_temp2["年"],
            low_temp2["num"],
            "o",
            color="lightcoral",
            label="低温",
            markersize=3,
        )

        low_temp3 = disasterTmp3[disasterTmp3["分类"] == "风速大"]
        ax2.plot(
            low_temp3["年"],
            low_temp3["num"],
            "^",
            color="#696969",
            label="风速大",
            markersize=3,
        )

        low_temp4 = disasterTmp4[disasterTmp4["分类"] == "干旱"]
        ax2.plot(
            low_temp4["年"],
            low_temp4["num"],
            "^",
            color="#E89F12",
            label="干旱",
            markersize=3,
        )
        ax2.set_ylim(0, 12)

        plt.title(f"灾害对{name}水稻单位面积产量的影响分析")
        plt.legend()
        img = draw_to_base64(fig)
        images.append(img)
    context.preview(
        {
            "type": "image",
            "data": images,
        }
    )
    return {"charts": images}


def draw_to_base64(fig):
    fig.canvas.draw()
    image_array = np.array(fig.canvas.renderer.buffer_rgba())
    image = Image.fromarray(image_array)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return f"data:image/png;base64,{base64.b64encode(img_byte_arr.read()).decode()}"
