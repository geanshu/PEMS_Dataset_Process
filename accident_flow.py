import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

data = np.load('./Tustin/22-01-01_22-01-21/PEMS_Tustin.npz')['data']
flow = data[:, :, 0].transpose(1, 0)
accident = data[:, :, 3].astype(int).transpose(1, 0)

flow_change = np.concatenate((np.zeros([data.shape[1], 1]), abs(np.diff(flow, axis=1))), axis=1) / flow * 100
flow_change_1 = np.concatenate((np.zeros([data.shape[1], 1]), abs(np.diff(flow_change))), axis=1) / flow_change * 100

flow = flow.flatten()
flow_change = flow_change.flatten()
flow_change_1 = flow_change_1.flatten()
accident = accident.flatten()

flow_acc = [flow[accident == l] for l in np.unique(accident)]
flow_change_acc = [flow_change[accident == l] for l in np.unique(accident)]
flow_change_1_acc = [flow_change_1[accident == l] for l in np.unique(accident)]

# plt.figure(dpi=500)
# flow-flow'
# plt.scatter(flow_change_acc[0], flow_acc[0], c='b', s=1, marker=',')  # 正常
# plt.scatter(flow_change_acc[1], flow_acc[1], c='r', s=1, marker='+')  # 事故
# plt.gca().xaxis.set_major_formatter(PercentFormatter())
# plt.ylabel('Flow (Veh/5 Minutes)')
# plt.xlabel('Flow Change(%)')
# plt.legend(['normal', 'accident'])
# plt.axis([0, 100, 0, 1000])

# plt.subplot(1, 2, 1)
# flow'-flow''
plt.scatter(flow_change_acc[0], flow_change_1_acc[0], c='b', s=1, marker=',')  # 正常
plt.scatter(flow_change_acc[1], flow_change_1_acc[1], c='r', s=1, marker='+')  # 事故
# plt.gca().xaxis.set_major_formatter(PercentFormatter())
# plt.gca().yaxis.set_major_formatter(PercentFormatter())
plt.ylabel("Flow Change Change(%)")
plt.xlabel('Flow Change(%)')
plt.legend(['normal', 'accident'])
plt.axis([0, 100, 0, 1000])

# plt.subplot(1, 2, 2)
# flow-flow''
# plt.scatter(flow_acc[0], flow_change_1_acc[0], c='b', s=1, marker=',')  # 正常
# plt.scatter(flow_acc[1], flow_change_1_acc[1], c='r', s=1, marker='+')  # 事故
# plt.gca().yaxis.set_major_formatter(PercentFormatter())
# plt.xlabel('Flow (Veh/5 Minutes)')
# plt.ylabel('Flow Change Change(%)')
# plt.legend(['normal', 'accident'])
# plt.axis([0, 1000, 0, 20])
plt.savefig('./accident_flow.png')
plt.show()
