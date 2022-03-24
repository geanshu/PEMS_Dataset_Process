import numpy as np

city = 'Tustin'
start_time, end_time = '2022-01-01 00:00', '2022-01-21 23:59'  # 数据下载开始于结束时间，每次下载一周，无数据则下载为空文件
time_str = start_time[2:10] + '_' + end_time[2:10]

save_path = r'./%s/' % city  # 文件保存路径
vds_list = np.genfromtxt(save_path + "%s_mainline.txt" % city, dtype=int)  # 需要下载的VDS列表
save_path = save_path + time_str + '/'


def create_PEMS_npz(path=save_path):
    incident = np.load(path + 'incident/incident.npz')['data']
    flow = np.load(path + 'combine/traffic.npz')['data']
    print('source shape:', incident.shape, flow.shape)
    data = np.concatenate((flow, incident), 2)

    print('target shape:', data.shape)
    np.savez(path + 'PEMS_%s.npz' % city, data=data)
    print('生成PEMS_%s.npz数据成功' % city)


if __name__ == '__main__':
    create_PEMS_npz()
