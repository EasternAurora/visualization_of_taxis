# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 12:07:20 2023

@author: win
"""

import os
import pandas as pd
from PIL import Image
import geopandas as gpd
import moviepy.editor as mp
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# 定义gif函数，用于绘制出租车行程分布GIF动图
def gif(name,cmap,timel):
    
    # 创建一个空的图像列表，用于存储每一帧的地图图像
    images = []
    
    count = 0
    # 遍历每个时间步
    for time in timel:
        count += 1
        # 选择当前时间步的数据
        file_name = r'frame\{}.shp'.format(time)
        current_data = gpd.read_file(file_name)

        # 绘制地图
        fig, ax = plt.subplots(figsize=(9, 9))
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.set_title(f'Time: {time}')

        # 根据车流量字段进行分层设色
        current_data.plot(ax=ax, column=name, cmap=cmap, edgecolor='black', linewidth=0.5, legend=True)

        # 保存地图为临时图像文件
        tmp_file = f'temp_{count}.png'
        plt.savefig(tmp_file, dpi=300)
        plt.close(fig)

        # 将临时图像文件加载到图像列表中
        images.append(Image.open(tmp_file))

    # 保存图像列表为GIF文件
    images[0].save(r'gif/{}_{}.gif'.format(timel[-1],name), save_all=True, append_images=images[1:], duration=500, loop=0, quantize=64)

    # 删除临时图像文件
    for image in images:
        image.close()
        image_path = image.filename
        if image_path.startswith('temp_'):
            os.remove(image_path)

# 定义 time_list函数，用于生成时间字符串
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

# 定义trans函数，用于将gif转化为mp4
def trans(name,timel):
    clip = mp.VideoFileClip(rf"gif\{timel[-1]}_{name}.gif")
    clip.write_videofile(rf"mp4\{timel[-1]}_{name}.mp4")

    # 设置颜色映射
cmap = LinearSegmentedColormap.from_list('custom_cmap', ['white', 'red'])
cmap1 = LinearSegmentedColormap.from_list('custom_cmap', ['white', 'blue'])

time_l=time_list('2023-03-01','2023-04-01',"1D",'%Y-%m-%d',0)

for i in range(len(time_l)-1):
    timel = time_list(f'{time_l[i]} 00:20:00',f'{time_l[i+1]} 00:00:00','20T','%Y-%m-%d %H:%M:%S',1)
    gif("PUN",cmap,timel)
    gif("DON",cmap1,timel)
    
    trans("PUN",timel)
    trans("DON",timel)
            