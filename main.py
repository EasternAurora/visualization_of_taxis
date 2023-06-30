# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 10:10:19 2023

@author: win
"""
import folium
import pandas as pd
from PIL import Image
import streamlit as st
import geopandas as gpd
from streamlit_folium import st_folium

# 定义paint函数，用于绘制map
def paint(time,name1,name2):
    
    m = folium.Map(location=[40.7,-74.0], zoom_start=10)

    file_name=r'frame\{}.shp'.format(time)
    current_data = gpd.read_file(file_name)
    
    #绘制出租车起始/终止点分布图
    cl=folium.Choropleth(
        geo_data=current_data,
        name='纽约市黄色出租车开始载客分布图',
        data=current_data,
        columns=['LocationID', name1],
        key_on='feature.properties.LocationID',
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='出租车数量/辆',
    ).add_to(m)

    cd=folium.Choropleth(
        geo_data=current_data,
        name='纽约市黄色出租车终止载客分布图',
        data=current_data,
        columns=['LocationID', name2],
        key_on='feature.properties.LocationID',
        fill_color='Blues',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='出租车数量/辆',
    ).add_to(m)
    
    #为出租车起始/终止点分布图添加tooltip功能
    tooltip = folium.GeoJsonTooltip(
    fields=['LocationID', name1],
    aliases=['区域编号: ', '出租车行程起始点数量: '],
    labels=True,
    sticky=False,
    )
    
    tooltip1 = folium.GeoJsonTooltip(
    fields=['LocationID', name2],
    aliases=['区域编号: ', '出租车行程终止点数量: '],
    labels=True,
    sticky=False,
    )
    
    cl.geojson.add_child(tooltip)
    cd.geojson.add_child(tooltip1)
    
    #加入图层控制器
    folium.LayerControl().add_to(m)

    return m

# 定义 time_list函数，用于生成时间字符串
def time_list(st,et,f,s):
    time_series = pd.date_range(start=st, end=et, freq=f)
    timel=[]
    for i in range(len(time_series)):
        time = time_series[i].strftime(s)
        rtime=time.replace(" ","_").replace("-","_").replace(":","_")
        timel.append(rtime)
    return timel

timel=time_list('2023-03-01 00:20:00','2023-04-01 00:00:00',"20T",'%Y-%m-%d %H:%M:%S')
timel1=time_list('2023-03-02 00:00:00','2023-04-01 00:00:00',"1D",'%Y-%m-%d %H:%M:%S')

# 网页初始设置为宽屏
st.set_page_config(layout="wide")

st.header("纽约市黄色出租车流量分析与可视化")
st.header("")
time1 = st.sidebar.selectbox('选择日期(24小时为单位)：',timel1)
time = st.sidebar.selectbox('选择时间(20分钟为单位)：',timel)
d={"开始载客":"PUN","终止载客":"DON"}
choice = st.sidebar.selectbox('选择出租车状态：',["开始载客","终止载客"])

col1,col2 = st.columns([1,1.29])

with col1:
    st.text("24小时内纽约市黄色出租车运营情况变化:")
    video_file = open(rf'mp4\{time1}_{d[choice]}.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

with col2:
    st.text("纽约市黄色出租车车流量日变化:")
    image = Image.open(rf'png/{time1}.png')
    st.image(image,width=300,use_column_width=True)

st.text("20分钟内纽约市黄色出租车运营分布:")
mt=paint(time,"PUN","DON")
output = st_folium(mt, width=1040, height=800)




