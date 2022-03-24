#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/14 21:23
# @Author  : Chenchen Wei
# @Description: 下载PeMS流量数据，一次下载一周数据

import time
import os
import numpy as np
import requests
from retrying import retry

city = 'Orange'
start_time, end_time = '2022-01-08 00:00', '2022-01-14 23:59'  # 数据下载开始于结束时间，每次下载一周，无数据则下载为空文件
time_str = start_time[2:10] + '_' + end_time[2:10]

save_path = r'./%s/' % city  # 文件保存路径
vds_list = np.genfromtxt(save_path + "%s.txt" % city, dtype=int)  # 需要下载的VDS列表
save_path = save_path + time_str + '/'


def time_2_timestamp(input, lags=True):
    """默认True: 时间转化为时间戳, 包含时差计算"""
    if lags:
        timeArray = time.strptime(input, "%Y-%m-%d %H:%M")
        # 转换成时间戳
        return int(time.mktime(timeArray) + 8 * 60 * 60)  # 时差计算
    else:
        time_local = time.localtime(input - 8 * 60 * 60)
        return time.strftime("%Y-%m-%d %H:%M", time_local)


def download(path, vds, start_time, end_time):
    start_stamp, end_stamp = time_2_timestamp(start_time), time_2_timestamp(end_time)
    i = 1
    for begin in range(start_stamp, end_stamp, 60 * 60 * 24 * 7):
        for type in ['flow', 'speed', 'occ']:
            url = get_url(vds, begin, type)
            download_data(path, url, i, type)
            print('Sleeping...')
            time.sleep(15)  # 下载完成休息五秒
        i += 1


@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=5000)
def download_data(path, url, i, type):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39"}
    data = {"redirect": "", "username": "aolong0714@outlook.com",
            "password": ":Uujazzy1@", "login": "Login"}
    session = requests.session()
    print('开始下载')
    response = session.post('https://pems.dot.ca.gov/', headers=headers, data=data)
    response = session.get(url)
    with open(path + '%s_%s.xlsx' % (vds, type), 'wb') as f:
        f.write(response.content)
        print('下载成功')


def get_url(vds, begin, type='flow'):
    str_begin = time_2_timestamp(begin, False)
    s_begin = str_begin[5:7] + '%2F' + str_begin[8:10] + '%2F' + str_begin[:4] + '+00%3A00',
    end = begin + 60 * 60 * 24 * 7 - 60
    str_end = time_2_timestamp(end, False)
    s_end = str_end[5:7] + '%2F' + str_end[8:10] + '%2F' + str_end[:4] + '+23%3A59',
    url = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&export=xls&station_id=' \
          + str(vds) + '&s_time_id=' + str(begin) + '&s_time_id_f=' + str(s_begin) + '&e_time_id=' + str(
        end) + '&e_time_id_f=' + str(
        s_end) + '&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6' \
                 '=on&holidays=on&q=' + type + '&q2=&gn=5min&agg=on'
    # print(url)
    print('获取url: vds[%s][%4s] %s --- %s %s' % (str(vds), type, str_begin, str_end, type))
    return url


if __name__ == '__main__':

    for vds in vds_list[23:]:
        save_paths = save_path + '/%s/' % str(vds)  # 创建文件保存路径
        if not os.path.exists(save_paths):
            os.makedirs(save_paths)
        print('开始下载：%s   %s---%s' % (str(vds), start_time, end_time))
        download(save_paths, vds, start_time, end_time)  # 下载文件
