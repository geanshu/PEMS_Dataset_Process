import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

data = np.load('./Tustin/22-01-01_22-01-21/PEMS_Tustin.npz')['data']
speed = data[:, :, 2]
accident = data[:, :, 3].astype(int)
speed_change = np.concatenate((abs(np.diff(speed, axis=0)), np.zeros([1, speed.shape[1]]))) / speed * 100
speed_change = np.concatenate((speed_change[-1].reshape(1, speed.shape[1]), speed_change[0:-1]))
# print(speed_change[-1].reshape(1,18).shape)
# print(speed_change[0:-1].shape)

speed = speed.flatten()
speed_change = speed_change.flatten()
accident = accident.flatten()

speed_0 = [speed[accident == l] for l in np.unique(accident)]
speed_change_0 = [speed_change[accident == l] for l in np.unique(accident)]

plt.figure(dpi=500)
plt.scatter(speed_change_0[0], speed_0[0], c='b', s=1, marker=',')  # 正常
plt.scatter(speed_change_0[1], speed_0[1], c='r', s=1, marker='+')  # 事故
plt.gca().xaxis.set_major_formatter(PercentFormatter())
plt.axis([0, 50, 0, 85])
plt.ylabel('Speed (mph)')
plt.xlabel('Speed Change(%)')
plt.legend(['normal', 'accident'])
plt.savefig('./accident_speed.png')
plt.show()
