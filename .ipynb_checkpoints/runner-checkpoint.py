from objects import economy
import numpy as np
import matplotlib.pyplot as plt

# build neighbors
N = 100

# must be friends with youself
neighbors = np.ones((N,N))

update_freq = 200
model = economy(N, N, neighbors, update_freq, 0.5, 0.02, 0.01)

for _ in range(1000000):
    model.next_period()

np.savetxt(f"save_{update_freq}.csv", np.array(model.save_history), delimiter=",")
np.savetxt(f"capital_{update_freq}.csv", np.array(model.capital_history), delimiter=",")
np.savetxt(f"consumption_{update_freq}.csv", np.array(model.consumption_history), delimiter=",")
np.savetxt(f"total_capital_{update_freq}.csv", np.array(model.total_capital_history), delimiter=",")

plt.plot(model.total_capital_history)
plt.xlabel("ticks (1 tick = 0.01 time units)")
plt.ylabel("total capital")
plt.show()
