# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 14:01:23 2023

@author: win
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# 定义statistic函数，用于统计
def statistic(timel,):
    y1 = []
    y2 = []
    for time in timel:
        df = gpd.read_file(rf"frame/{time}.shp")
        pun = df["PUN"].values.sum()
        don = df["DON"].values.sum()
        y1.append(pun)
        y2.append(don)
    plt.clf()
    plt.figure(figsize=(20, 15))
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.plot(timel, y1,label="出租车开始载客数")
    plt.plot(timel, y2,label="出租车终止载客数")
    plt.xticks(range(len(timel)), timel , rotation='vertical')
    plt.xlabel('时间')
    plt.ylabel('黄色出租车数量/辆')
    plt.legend()
    plt.savefig(rf"png/{timel[-1]}.png")

# 定义time_list函数，用于生成时间字符串
def time_list(st,et,f,s,c):
    time_series = pd.date_range(start=st, end=et, freq=f)
    timel=[]
    for i in range(len(time_series)):
        time = time_series[i].strftime(s)
        if c==1:
            rtime = time.replace(" ","_").replace("-","_").replace(":","_")
        else:
            rtime=time
        timel.append(rtime)
    return timel

time_l=time_list('2023-03-01','2023-04-01',"1D",'%Y-%m-%d',0)
for i in range(len(time_l)-1):
    timel = time_list(f'{time_l[i]} 00:20:00',f'{time_l[i+1]} 00:00:00','20T','%Y-%m-%d %H:%M:%S',1)
    statistic(timel)
