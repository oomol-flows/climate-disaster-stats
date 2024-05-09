import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Source Han Sans SC"]

# 使用pandas读取原始数据
def read_csv_file(file_path):
    # 读取CSV文件
    data = pd.read_csv(file_path)
    return data

#计算正态分布每周的均值和标准差
def calculate_weekly_stats(data: pd.DataFrame, dType="temp"):
    # 将日期列转换为日期格式
    data['日期'] = pd.to_datetime(data['日期'], format='%Y%m%d')

    # 添加一个新的列来表示每年的周数
    data['周'] = data['日期'].dt.isocalendar().week

    # 筛选出2001年至2009年的数据
    data = data[(data['日期'].dt.year >= 2001) & (data['日期'].dt.year <= 2009)]

    # 按周分组，计算每周的均值和标准差
    if dType=="temp":
        weekly_stats = data.groupby('周')['气温'].agg(['mean', 'std'])
    elif dType=="precipitation":
        weekly_stats = data.groupby('周')['降水'].agg(['mean', 'std'])
    elif dType=="wind":
        weekly_stats = data.groupby('周')['平均风速'].agg(['mean', 'std'])
    elif dType=="humidity":
        weekly_stats = data.groupby('周')['平均湿度'].agg(['mean', 'std'])

    return weekly_stats

#对灾害类型进行分类
def classify_data(data: pd.DataFrame, weekly_stats, dType="temp",sigma1=2,sigma2=2):
    """
    sigma1:调整1-4月，10-12月正态分布评估标准的标准差范围，数值越小，灾害越多
    sigma2:调整5-9月正态分布评估标准的标准差范围，数值越小，灾害越多
    """
    # 将日期列转换为日期格式
    data['日期'] = pd.to_datetime(data['日期'], format='%Y%m%d')

    # 添加一个新的列来表示每年的周数
    data['周'] = data['日期'].dt.isocalendar().week

    # 筛选出2010年至2020年的数据
    data = data[(data['日期'].dt.year >= 2010) & (data['日期'].dt.year <= 2020)]

    if dType=="wind":
        data['分类'] = np.select(
            [
                ((data['周'].map(weekly_stats['mean']) + sigma1 * data['周'].map(weekly_stats['std'])) < data['平均风速']) & (((data['日期'].dt.month >= 1) & (data['日期'].dt.month <= 4)) | ((data['日期'].dt.month >= 10) & (data['日期'].dt.month <= 12))),
                ((data['周'].map(weekly_stats['mean']) + sigma2 * data['周'].map(weekly_stats['std'])) < data['平均风速']) & ((data['日期'].dt.month >= 5) & (data['日期'].dt.month <= 9)),
                ((data['周'].map(weekly_stats['mean']) - sigma1 * data['周'].map(weekly_stats['std'])) > data['平均风速']) & (((data['日期'].dt.month >= 1) & (data['日期'].dt.month <= 4)) | ((data['日期'].dt.month >= 10) & (data['日期'].dt.month <= 12))),
                ((data['周'].map(weekly_stats['mean']) - sigma2 * data['周'].map(weekly_stats['std'])) > data['平均风速']) & ((data['日期'].dt.month >= 5) & (data['日期'].dt.month <= 9))
            ], 
            ['风速大', '风速大', '风速小', '风速小'], 
            default='正常' 
        )
    elif dType=="temp":
        data['分类'] = np.select(
            [
                ((data['周'].map(weekly_stats['mean']) + sigma1 * data['周'].map(weekly_stats['std'])) < data['气温']) & (((data['日期'].dt.month >= 1) & (data['日期'].dt.month <= 4)) | ((data['日期'].dt.month >= 10) & (data['日期'].dt.month <= 12))),
                ((data['周'].map(weekly_stats['mean']) + sigma2 * data['周'].map(weekly_stats['std'])) < data['气温']) & ((data['日期'].dt.month >= 5) & (data['日期'].dt.month <= 9)),
                ((data['周'].map(weekly_stats['mean']) - sigma1 * data['周'].map(weekly_stats['std'])) > data['气温']) & (((data['日期'].dt.month >= 1) & (data['日期'].dt.month <= 4)) | ((data['日期'].dt.month >= 10) & (data['日期'].dt.month <= 12))),
                ((data['周'].map(weekly_stats['mean']) - sigma2 * data['周'].map(weekly_stats['std'])) > data['气温']) & ((data['日期'].dt.month >= 5) & (data['日期'].dt.month <= 9))
            ], 
            ['高温', '高温', '低温', '低温'], 
            default='正常'
        )
    elif dType=="humidity":
        data['分类'] = np.select(
            [
                ((data['周'].map(weekly_stats['mean']) + sigma1 * data['周'].map(weekly_stats['std'])) < data['平均湿度']) & (((data['日期'].dt.month >= 1) & (data['日期'].dt.month <= 4)) | ((data['日期'].dt.month >= 10) & (data['日期'].dt.month <= 12))),
                ((data['周'].map(weekly_stats['mean']) + sigma2 * data['周'].map(weekly_stats['std'])) < data['平均湿度']) & ((data['日期'].dt.month >= 5) & (data['日期'].dt.month <= 9)),
                ((data['周'].map(weekly_stats['mean']) - sigma1 * data['周'].map(weekly_stats['std'])) > data['平均湿度']) & (((data['日期'].dt.month >= 1) & (data['日期'].dt.month <= 4)) | ((data['日期'].dt.month >= 10) & (data['日期'].dt.month <= 12))),
                ((data['周'].map(weekly_stats['mean']) - sigma2 * data['周'].map(weekly_stats['std'])) > data['平均湿度']) & ((data['日期'].dt.month >= 5) & (data['日期'].dt.month <= 9))
            ], 
            ['湿润', '湿润', '干旱', '干旱'], 
            default='正常'
        )
    else:
        data['分类'] = np.select(
            [
                ((data['周'].map(weekly_stats['mean']) + sigma1 * data['周'].map(weekly_stats['std'])) < data['降水']) & (((data['日期'].dt.month >= 1) & (data['日期'].dt.month <= 4)) | ((data['日期'].dt.month >= 10) & (data['日期'].dt.month <= 12))),
                ((data['周'].map(weekly_stats['mean']) + sigma2 * data['周'].map(weekly_stats['std'])) < data['降水']) & ((data['日期'].dt.month >= 5) & (data['日期'].dt.month <= 9)),
                ((data['周'].map(weekly_stats['mean']) - sigma1 * data['周'].map(weekly_stats['std'])) > data['降水']) & (((data['日期'].dt.month >= 1) & (data['日期'].dt.month <= 4)) | ((data['日期'].dt.month >= 10) & (data['日期'].dt.month <= 12))),
                ((data['周'].map(weekly_stats['mean']) - sigma2 * data['周'].map(weekly_stats['std'])) > data['降水']) & ((data['日期'].dt.month >= 5) & (data['日期'].dt.month <= 9))
            ], 
            ['降水多', '降水多', '降水少', '降水少'], 
            default='正常'
        )

    data['日期']=pd.to_datetime(data['日期'],format='%Y%m%d')

    data['周'] = data['日期'].dt.isocalendar().week
    data['月'] = data['日期'].dt.month
    data['年'] = data['日期'].dt.year
    data['周'] = data.groupby(['月'])['周'].transform(lambda x: pd.factorize(x)[0] + 1)
    return data

#保存灾害类型数据
def saveDisaster(data,indicator,folder_path):
     file_path=folder_path+"{}_disaster.csv".format(indicator)
     data.to_csv(file_path.format(indicator),index=False)

#绘制综合灾害图像
def draw_pic(yieldData: pd.DataFrame ,disasterData: list[pd.DataFrame]):
    grouped = yieldData.groupby('name')
    #读取灾害数据
    df1,df2,df3,df4=disasterData[1],disasterData[0],disasterData[2],disasterData[3]

    # Generate and save the plots for each area
    for name, group in grouped:
        
        disasterTmp = df1[df1['市'] == name]

        disasterTmp = disasterTmp[['周', '分类', '月','日期']]

        disasterTmp['num'] = (disasterTmp['周'] - 1) / 4 + (disasterTmp['月'] - 1)

        disasterTmp['年'] = pd.to_datetime(disasterTmp['日期']).dt.year
        
        disasterTmp = disasterTmp[disasterTmp['分类'].isin(['降水多', '降水少'])]

        disasterTmp2 = df2[df2['市'] == name]
        
        disasterTmp2 = disasterTmp2[['周', '分类', '月','日期']]
        
        disasterTmp2['num'] = (disasterTmp2['周'] - 1) / 4 + (disasterTmp2['月'] - 1)

        disasterTmp2['年'] = pd.to_datetime(disasterTmp2['日期']).dt.year
        
        disasterTmp2 = disasterTmp2[disasterTmp2['分类'].isin(['高温', '低温'])]

        disasterTmp3 = df3[df3['市'] == name]
        
        disasterTmp3 = disasterTmp3[['周', '分类', '月','日期']]
        
        disasterTmp3['num'] = (disasterTmp3['周'] - 1) / 4 + (disasterTmp3['月'] - 1)
        disasterTmp3['年'] = pd.to_datetime(disasterTmp3['日期']).dt.year
        disasterTmp3 = disasterTmp3[disasterTmp3['分类'].isin(['风速大', '风速小'])]

        disasterTmp4 = df4[df4['市'] == name]
        
        disasterTmp4 = disasterTmp4[['周', '分类', '月','日期']]

        disasterTmp4['年'] = pd.to_datetime(disasterTmp4['日期']).dt.year
        disasterTmp4['num'] = (disasterTmp4['周'] - 1) / 4 + (disasterTmp4['月'] - 1)
        disasterTmp4 = disasterTmp4[disasterTmp4['分类'].isin(['湿润', '干旱'])]
            

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        # # Plot yieldPerArea vs year
        ax1.bar(list(group['year']), list(group['yieldPerArea']), label=name, color='black', alpha=0.3)
        ax1.set_xlabel('年份')
        ax1.set_ylabel('水稻单位面积产量')

        high_temp = disasterTmp[disasterTmp['分类'] == '降水多']
        ax2.plot(high_temp['年'], high_temp['num'], 's',color='b',label='降水多', markersize=3)
        ax2.set_ylabel('月份')

        low_temp = disasterTmp[disasterTmp['分类'] == '降水少']
        ax2.plot(low_temp['年'], low_temp['num'], 's', color='cornflowerblue',label='降水少', markersize=3)


        high_temp2 = disasterTmp2[disasterTmp2['分类'] == '高温']
        ax2.plot(high_temp2['年'], high_temp2['num'], 'o', color='darkred', label='高温', markersize=3)


        low_temp2 = disasterTmp2[disasterTmp2['分类'] == '低温']
        ax2.plot(low_temp2['年'], low_temp2['num'], 'o', color='lightcoral', label='低温', markersize=3)


        low_temp3 = disasterTmp3[disasterTmp3['分类'] == '风速大']
        ax2.plot(low_temp3['年'], low_temp3['num'], '^', color='#696969', label='风速大', markersize=3)

            
        low_temp4 = disasterTmp4[disasterTmp4['分类'] == '干旱']
        ax2.plot(low_temp4['年'], low_temp4['num'], '^', color='#E89F12', label='干旱', markersize=3)
        ax2.set_ylim(0, 12)

        plt.title(f'灾害对{name}水稻单位面积产量的影响分析')
        plt.legend()
        plt.show()
        # fig = plt.figure(
        #   figsize=(400/200, 400/200),
        #   dpi=200
        # )
        return draw_to_base64(fig)


def draw_to_base64(fig):
    fig.canvas.draw()
    image_array = np.array(fig.canvas.renderer.buffer_rgba())
    image = Image.fromarray(image_array)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")

def main(inputs: dict, context):
  # indicator_list=["humidity"]
  disasterList: list[pd.DataFrame]=[]
  for indicator in inputs["indicators"]:
      file_path="{}/{}_result.csv".format(inputs["climate_data_dir"], indicator)
      tempData=read_csv_file(file_path)
      #计算灾害异常
      weeklyStatsData=calculate_weekly_stats(tempData,dType=indicator)
      #给灾害分类
      disaster=classify_data(tempData, weeklyStatsData, sigma1=3, sigma2=2, dType=indicator)
      disasterList.append(disaster)
      #保存灾害数据
      # saveDisaster(disaster,indicator,"/climate/assets/saveData")
      #读取产量数据
  
  yieldData=pd.read_csv(inputs["yield_data"])
  pic = draw_pic(yieldData, disasterList)
  context.output(pic, "chart", True)
