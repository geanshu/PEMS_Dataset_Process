# import os

# with open("I80-E.txt", "r") as f:
#     data = f.readlines()
#     data =eval(data)
    # print(data)

import numpy as np
import pandas as pd
import requests
import os

# data = np.genfromtxt("d:/Shu/dataset/I80-E.txt",dtype=int)  # 将文件中数据加载到data数组里
# print(data)
# print(data[0])

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
# data = {"redirect": "", "username": "aolong0714@outlook.com",
#         "password": ":Uujazzy1@", "login": "Login"}
# url = "http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&export=xls&station_id=402814&s_time_id=1640995200&s_time_id_f=('01%2F01%2F2022+00%3A00',)&e_time_id=1641599940&e_time_id_f=('01%2F07%2F2022+23%3A59',)&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=flow&q2=speed&gn=5min&agg=on"
# session = requests.session()
# response = session.post("https://pems.dot.ca.gov/", headers=headers, data=data)
# response = session.get(url, headers=headers)
# print(response)
# fp = open("1.xlsx", "wb")
# fp.write(response.content)
# fp.close()

if __name__ == '__main__':
    save_path = r'./'  # 文件保存路径
    # vds_list = [602467, 602468]  # 需要下载的VDS列表
    vds_list = np.genfromtxt("./Tustin.txt",dtype=int) # 需要下载的VDS列表
    start_time, end_time = '2022-01-01 00:00', '2022-01-07 23:59'  # 数据下载开始于结束时间，每次下载一周，无数据则下载为空文件
    name = start_time[2:10] + '_' + end_time[2:10]
    
    for vds in vds_list:
        save_paths = save_path + name + '/' + str(vds) + '/' # 创建文件保存路径
        if os.path.exists(save_paths+ '%d_combine.csv'% vds ):
            os.remove(save_paths+ '%d_combine.csv'% vds )