import numpy as np
import pandas as pd
import os
import sys

city = 'Tustin'
start_time, end_time = '2022-01-01 00:00', '2022-01-21 23:59'  # 数据下载开始于结束时间
time_str = start_time[2:10] + '_' + end_time[2:10]

save_path = r'./%s/' % city  # 文件保存路径
vds_list = np.genfromtxt(save_path + "%s_mainline.txt" % city, dtype=int)  # 需要下载的VDS列表
save_path = save_path + time_str + '/'


def combine_feature(path, vds, i):
    init = pd.read_excel(path + '%d/%d_flow.xlsx' % (vds, i), index_col=None)
    init = init.drop(columns=['# Lane Points', '% Observed', '5 Minutes'])

    init['Occupancy (%)'] = pd.read_excel(path + '%d/%d_occ.xlsx' % (vds, i), index_col=None)['Occupancy (%)'].apply(
        lambda x: abs(x / 100)).copy()
    init['Speed (mph)'] = pd.read_excel(path + '%d/%d_speed.xlsx' % (vds, i), index_col=None)['Speed (mph)'].copy()

    return init


def combine_download_data(vds, path):
    num = int(len(os.listdir(path + '%d/' % vds)) / 3)
    dfs = combine_feature(path, vds, 1)
    for i in range(2, num + 1):
        df = combine_feature(path, vds, i)
        dfs = np.row_stack((dfs, df))
    pd.DataFrame(dfs).to_csv(path + 'combine/%d_combine.csv' % vds, index=None, header=None)


def merge(path=save_path):
    if not os.path.exists(path + 'combine/'):
        os.makedirs(path + 'combine/')

    for vds in vds_list:
        if not os.path.exists(path):
            sys.stderr.write("No such file\n")
            pass
        print('start merge data：%s   %s---%s' % (str(vds), start_time, end_time))
        combine_download_data(vds, path)  # 将单个VDS下载文件进行合并
        print('merge succeed!')


def create_traffic_npz(path=save_path):
    print('开始生成traffic.npz')
    target = pd.read_csv(path + 'combine/%d_combine.csv' % vds_list[0], index_col=None, header=None).values
    # print(target.shape)
    target = target[np.newaxis, :]
    for vds in vds_list[1:]:
        df = pd.read_csv(path + 'combine/%d_combine.csv' % vds, index_col=None, header=None).values
        df = df[np.newaxis, :]
        target = np.concatenate((target, df), 0)

    target = np.transpose(target, [1, 0, 2])
    np.savez(path + 'combine/traffic.npz', data=target)
    print(target.shape)
    print('生成traffic.npz数据成功')


if __name__ == '__main__':
    merge()
    create_traffic_npz()

