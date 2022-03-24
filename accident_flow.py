import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

data = np.load('./Tustin/22-01-01_22-01-21/PEMS_Tustin.npz')['data']
flow = data[:, :, 0]
accident = data[:, :, 3].astype(int)
flow_change = np.concatenate((abs(np.diff(flow, axis=0)), np.zeros([1, flow.shape[1]]))) / flow * 100
flow_change = np.concatenate((flow_change[-1].reshape(1, 18), flow_change[0:-1]))

flow = flow.flatten()
flow_change = flow_change.flatten()
accident = accident.flatten()

flow_0 = [flow[accident == l] for l in np.unique(accident)]
flow_change_0 = [flow_change[accident == l] for l in np.unique(accident)]

plt.figure(dpi=500)
plt.scatter(flow_change_0[0], flow_0[0], c='b', s=1, marker=',')  # 正常
plt.scatter(flow_change_0[1], flow_0[1], c='r', s=1, marker='+')  # 事故
plt.gca().xaxis.set_major_formatter(PercentFormatter())
plt.axis([0, 100, 0, 1000])

plt.ylabel('Flow (Veh/5 Minutes)')
plt.xlabel('Flow Change(%)')
plt.legend(['normal', 'accident'])
plt.savefig('./accident_flow.png')
plt.show()
