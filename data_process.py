# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 18:59:44 2023

@author: win
"""

import pandas as pd
import geopandas as gpd
import pyarrow.parquet as pq

# 定义group函数，用于按上车/下车时间和起始/终止点ID分割元数据
def group(df,key1,key2):
    
    # 以20分钟为间隔分组元数据
    df.sort_values(by=key1,inplace=True)
    grouped_df = df.groupby(pd.Grouper(key=key1,freq='20Min'))

    grouped_dataframes = []
    for name, group in grouped_df:
        sub_grouped_dataframes = []
        
        # 按起始/终止点ID分组元数据
        sub_grouped_df = group.groupby(key2)
        for sub_name, sub_group in sub_grouped_df:

            sub_group_df = pd.DataFrame(sub_group)
            sub_grouped_dataframes.append(sub_group_df)
        grouped_dataframes.append(sub_grouped_dataframes)
    return grouped_dataframes

# 定义clean函数，用于清洗分组后数据
def clean(df,time_series,n):
    location = []
    for i in range(len(df)):
        
        #sub_location键0对应的值为当前帧的时间
        sub_location = {0:time_series[i]}
        for j in range(len(df[i])):
            
            #统计当前帧内，出租车数量的累计值
            ll = len(df[i][j])
            sub_location[df[i][j].iloc[0,n]]=ll
        location.append(sub_location)
    return location

# 定义rewrite函数，用于将清洗后数据写入出租车区域的shipfile中
def rewrite(file,l1,l2,name1,name2,i):
    gdc = gpd.read_file(file)
    
    #新建字段”time“，写入当前帧的时间
    gdc["time"] = l1[i][0].strftime('%Y-%m-%d %H:%M:%S')
    
    #新建两个字段”PUN“和”DON“，分别写入区域内上客和下客的出租车数量
    if gdc.iloc[0,4] in l1[i].keys():
        gdc[name1] = l1[i][gdc.iloc[0,4]]
    else:
        gdc[name1] = 0
    if gdc.iloc[0,4] in l2[i].keys():
        gdc[name2] = l2[i][gdc.iloc[0,4]]
    else:
        gdc[name2] = 0
    
    output_file = r'rewrite\{}_{}.shp'.format(i+1,gdc.iloc[0,4])
    gdc.to_file(output_file)
    
# 定义unite函数，以帧（20min）为单位，读取已经出租车行程数据的shipfile文件，并合并成一个GeoDataFrame
def unite(n1,n2):
    zones_l = []
    for i in range(n1,n2):
        for j in range(1,264):
            file_name = r'rewrite\{}_{}.shp'.format(i,j)
            gdf = gpd.read_file(file_name)
            zones_l.append(gdf)
    data = pd.concat(zones_l)

    time_values = sorted(data['time'].unique())
    for time in time_values:
        current_data = data[data['time'] == time]
        rtime = time.replace(" ","_").replace("-","_").replace(":","_")
        output_file = r"frame\{}.shp".format(rtime)
        current_data.to_file(output_file)

# 读取2023年3月纽约市黄色出租车行程数据（最新数据），将其转化为DataFrame
df = pq.read_table(r"yellow_tripdata_2023-03.parquet").to_pandas()

# 限制数据时间
t1 = pd.to_datetime("2023-03-01 00:00:00")
t2 = pd.to_datetime("2023-04-01 00:00:00")
df = df[df['tpep_pickup_datetime']<t2]
df = df[df['tpep_pickup_datetime']>t1]
df = df[df['tpep_dropoff_datetime']<t2]
df = df[df['tpep_dropoff_datetime']>t1]

pud = group(df,'tpep_pickup_datetime','PULocationID')
dod = group(df,'tpep_dropoff_datetime','DOLocationID')

print("出租车数据分类完毕！")

# 设置初始时间和结束时间
start_time = '2023-03-01 00:20:00'
end_time = '2023-04-01 00:00:00'

# 生成时间序列
time_series = pd.date_range(start=start_time, end=end_time, freq='20T')

print("生成时间序列完毕！")

pul = clean(pud,time_series,7)
dol = clean(dod,time_series,8)

#读取纽约市出租车区域
data = gpd.read_file(r'taxi_zones\taxi_zones.shp')

#shipfile中区域编号与TLC给出的区域编号有所出入，修改部分区域编号
data.iloc[56,4]=57
data.iloc[103,4]=104
data.iloc[104,4]=105

# 根据区域编号进行分割
values = data["LocationID"].values

# 分割并保存每个子集为独立的shipfile文件
for value in values:
    subset = data[data["LocationID"] == value]
    output_file = r'shipfile\{}.shp'.format(value)
    subset.to_file(output_file, driver='ESRI Shapefile')

print("出租车区域分割完毕！")

# 使用rewrite函数
for i in range(2232):
    for j in range(1,264):
        file=r'shipfile\{}.shp'.format(j)
        rewrite(file,pul,dol,"PUN","DON",i)

print("出租车行程数据写入完毕！")

# 使用unite函数
for i in range(31):
    unite(i*72+1,(i+1)*72+1)

print("数据处理全部完成！")
