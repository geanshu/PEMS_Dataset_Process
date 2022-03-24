import numpy as np
import pandas as pd
import datetime
import copy

city = 'Tustin'
start_time, end_time = '2022-01-01 00:00', '2022-01-21 23:59'  # 数据下载开始于结束时间
time_str = start_time[2:10] + '_' + end_time[2:10]

save_path = r'./%s/' % city  # 文件保存路径
vds_list = np.genfromtxt(save_path + "%s_mainline.txt" % city, dtype=int)  # 需要下载的VDS列表
save_path = save_path + time_str + '/'


def dataInterval(incident):
    start = datetime.datetime.strptime(incident['Start Time'], '%m-%d-%y %H:%M')
    duration = datetime.timedelta(minutes=int(incident['Duration (mins)']))
    end = start + duration

    incident['Start Time'] = (start.day - 1) * 24 * 60 / 5 + start.hour * 60 / 5 + int(start.minute / 5)
    incident['End Time'] = (end.day - 1) * 24 * 60 / 5 + end.hour * 60 / 5 + int(end.minute / 5)
    return incident


def pre_process_incident(path=save_path):
    incident = pd.read_excel(path + 'incident.xlsx', index_col=None)
    incident = incident.drop(columns=['Incident Id', 'Source', 'AREA', 'LOCATION', 'DESCRIPTION'])

    incident = incident.apply(dataInterval, axis=1)
    incident = incident.drop(columns=['Duration (mins)', 'CA PM'])
    incident = incident.loc[:, ['Start Time', 'End Time', 'Freeway', 'Abs PM']]

    incident = incident.groupby('Freeway')
    for (name, data) in incident:
        data = data.drop(columns='Freeway')
        data.to_excel(path + '%s.xlsx' % name, index=None)
    print('incident preprocess succeed!')
    return


def create_incident_npz(path=save_path):
    print('start create incident.npz')
    info = pd.read_excel('./%s/%s.xlsx' % (city, city), index_col=None)
    info = info[info.Type.isin(['Mainline'])]
    info = info.drop(
        columns=['District', 'County', 'City', 'CA PM', 'Length', 'Name', 'Lanes', 'Sensor Type', 'HOV', 'MS ID',
                 'IRM', 'Type'])

    data = np.zeros([len(vds_list), int(3 * 7 * 24 * 60 / 5), 1], dtype=np.float64)

    for (Fwy, sensor) in info.groupby('Fwy'):
        incident = pd.read_excel(path + '%s.xlsx' % Fwy, index_col=None, names=None)
        for row in incident.itertuples():
            Abs_PM = getattr(row, '_3')
            if Fwy[-1] == 'N':
                sensor['len'] = sensor['Abs PM'].apply(lambda x: x - Abs_PM)
            elif Fwy[-1] == 'S':
                sensor['len'] = sensor['Abs PM'].apply(lambda x: Abs_PM - x)
            if len(sensor[sensor.len >= 0]) > 0:
                idx = sensor[sensor.len >= 0]['len'].argmin()
            else:
                idx = sensor['len'].argmax()

            # idx = sensor_tmp['len'].argmin()
            id = int((sensor['ID'].iloc[[idx]].values)[0])

            id_idx = (np.argwhere(vds_list == id))[0][0]
            data[id_idx][getattr(row, '_1'):getattr(row, '_2')] = 1
        # print(sensor)
    data = np.transpose(data, [1, 0, 2])
    print(data.shape)
    np.savez(path + 'incident.npz', data=data)
    print('create incident.npz succeed!')
    return


if __name__ == '__main__':
    # pre_process_incident(save_path + 'incident/')
    create_incident_npz(save_path + 'incident/')
    # print(np.argwhere(data == True))
