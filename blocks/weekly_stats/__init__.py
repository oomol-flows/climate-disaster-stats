import pandas as pd
import os
import tempfile

def main(inputs: dict, context):
  # TODO 支持直传 dataframe
  data = pd.read_pickle(inputs["climate_data"])
  
  # 将日期列转换为日期格式
  data['日期'] = pd.to_datetime(data['日期'], format='%Y%m%d')
  
  # 添加一个新的列来表示每年的周数
  data['周'] = data['日期'].dt.isocalendar().week
  
  # 筛选出2001年至2009年的数据
  data = data[(data['日期'].dt.year >= inputs["year_from"]) & (data['日期'].dt.year <= inputs["year_to"])]
  
  # 按周分组，计算每周的均值和标准差
  weekly_stats = data.groupby('周')[inputs["indicator"]].agg(['mean', 'std'])
  
   # TODO 支持直传 dataframe
  pkl = os.path.join(tempfile.gettempdir(), "weekly_stats_{}.pkl".format(hash(inputs["climate_data"])))
  weekly_stats.to_pickle(pkl)
  
   # TODO 支持直传 dataframe
  context.output(pkl, "stats", True)
