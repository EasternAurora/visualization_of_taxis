# visualization_of_taxis
An GIS' development.
程序说明，共有4页，编辑时间：2023年6月12日星期一，编辑者：刘丙南。

数据来源：纽约市出租车和豪华轿车委员会（TLC）。

数据简介：
（1）纽约市黄色出租车轨迹记录（Yellow Taxi Trip Records）：记录纽约市黄色出租车轨迹的parquet文件，本次选择TLC公布的最新2023年3月共计31天的记录，应用字段为tpep_pickup_datatime(美国东部时间乘客上车时刻)、tpep_dropoff_datatime（美国东部时间乘客下车时刻）、PULocationID（乘客上车区域编号）、DOLocationID（乘客下车区域编号），共计3403766条数据。
（2）纽约市出租车运营区域（TLC Taxi Zones）：TLC发布的包含纽约市263个出租车运营区域的shipfile文件，应用字段为LocationID（区域编号）。

文件说明：data_process.py用于处理元数据，mp4.py用于生成车流量日变化MP4，statistic.py用于统计车流量并绘制折线图，main.py为主程序。taxi_zones文件夹中为纽约市出租车运营区域（TLC Taxi Zones）数据，yellow_tripdata_2023-03.parquet为2023年3月纽约市黄色出租车轨迹记录（Yellow Taxi Trip Records）。frame文件夹用于储存处理后的数据，rewrite文件夹用于储存处理过程中的数据。gif、mp4和png文件夹储存可视化结果。

主程序运行依赖库：folium、pandas、PIL、streamlit、geopandas、streamlit_folium。
数据处理依赖库：os、pandas、geopandas、moviepy.editor、PIL、matplotlib.pyplot、matplotlib.colors、pyarrow.parquet。
（数据处理部分已经完成，可以直接通过streamlit运行主程序main.py）

应用目标：纽约市黄色出租车流量分析与可视化。

主程序界面操作：
（1）选择参数：日期（以天为单位）、时间（以20分钟为单位）和出租车状态。日期参数和时间参数格式为：年_月_日_小时_分钟_秒。用户选择的日期参数和时间参数均为截止时间，例如，选择日期参数为2023_03_02_00_00_00，将会显示2023_03_01_00_00_00到2023_03_02_00_00_00这一时间段内的24小时纽约市黄色出租车运营情况变化和纽约市黄色出租车车流量日变化折线图。同理，选择时间参数后，将会显示截至选择时间的20分钟内（一帧）纽约市黄色出租车运营分布图，该图为24小时纽约市黄色出租车运营情况变化的一帧。出租车状态则决定了显示的是停止载客出租车数量还是开始载客出租车数量，仅对24小时纽约市黄色出租车运营情况变化有影响。

（2）24小时内纽约市黄色出租车运营情况变化：格式为mp4，显示纽约市各区域停止载客出租车数量或开始载客出租车数量，单位为量。视频进度条上方有放大按钮。

（3）纽约市黄色出租车车流量日变化：蓝线为纽约市各区域停止载客出租车总数量，黄线为开始载客出租车总数量。x轴为时间，最小刻度之间间隔20分钟，即为24小时纽约市黄色出租车运营情况变化的一帧。右上角有放大按钮。

（4）20分钟内纽约市黄色出租车运营分布：详细显示了24小时内纽约市黄色出租车运营情况变化每一帧的具体信息将鼠标放置于每个区域上时即显示当前区域编号和不同状态下出租车数量。右上角图层控制器可以选择出租车状态。注意，底图来自OSM。


程序流程图：

![思维导图](https://github.com/EasternAurora/visualization_of_taxis/assets/135222933/79dee58b-b893-4bf0-bbd9-78dc9f8f49a2)
