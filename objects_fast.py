import numpy as np

class Economy:
    """Agent-based Solow economy with heterogeneous saving rates and social learning.

    N households each supply Labour/N units of labour and own capital. Output is
    Cobb-Douglas, Y = K^alpha * L^(1 - alpha), and factors are paid their marginal
    products. Each tick, households earn income, save a fraction s_i of it,
    consume the rest, and their capital depreciates. Occasionally a household
    copies the saving rate of its highest-consuming neighbour, plus small noise.

    Args:
        N (int): Number of households.
        Labour (float): Total labour supply, split equally across households.
        capital_pc (float): Initial capital per household.
        neighbors (np.ndarray): N x N 0/1 adjacency matrix; neighbors[i, j] = 1
            if j is a neighbour of i. The diagonal should be 1 (each household
            is its own neighbour).
        update_freq (float): Mean time between saving-rate updates for a
            household (each tick, the update probability is dt / update_freq).
        alpha (float): Capital share of output, in (0, 1).
        dep (float): Depreciation rate per unit time.
        dt (float): Real time per tick; dt -> 0 approaches continuous time.
            1/dt should be an integer.
        

    Attributes:
        total_capital (float): Aggregate capital stock.
        household_save (np.ndarray): Saving rates, shape (N,), in [0, 1].
        household_capital (np.ndarray): Capital holdings, shape (N,).
        household_consumption (np.ndarray): Consumption in the last tick
            (a flow over dt, not a per-unit-time rate), shape (N,).
        tick (int): Number of ticks elapsed.
        save_history, capital_history, consumption_history,
        total_capital_history (list): Snapshots taken once per unit of time
            (every 1/dt ticks), recording the state at the start of that tick.
    """
    def __init__(self, N, Labour, capital_pc, neighbors, update_freq, alpha, dep, dt, seed):
        self.N = N
        self.Labour = Labour
        self.neighbors = neighbors
        self.total_capital = N* capital_pc
        self.update_freq = update_freq
        self.alpha = alpha
        self.dep = dep
        self.dt = dt
        self.seed = seed

        self.save_history = []
        self.capital_history = []
        self.consumption_history = []
        self.total_capital_history = []
        self.tick = 0
        self.update_every = int(round(1/dt))
        

        # Set up numpy arrays for the households
        self.household_save = self.seed.uniform(0,1,size=self.N)
        self.household_capital = np.full(self.N, capital_pc)
        self.household_consumption = np.zeros(self.N)



    def next_tick(self):

        """Advance the economy by one tick (dt units of time).

        1. Compute the interest rate r and wage w from aggregate capital.
        2. Households receive income, save fraction s_i, consume the rest;
           capital depreciates at rate dep.
        3. Each household, with probability dt / update_freq, adopts the saving
           rate of its highest-consuming neighbour. If that rate differs from
           its own, U(-0.01, 0.01) noise is added and the result clipped to [0, 1].
        4. Every 1/dt ticks, append the pre-tick state to the history lists.
        """
        
        r = self.alpha * self.total_capital ** (self.alpha -1) * self.Labour **(1-self.alpha)
        w = (1-self.alpha) * self.total_capital ** (self.alpha) * self.Labour **(-self.alpha)

        initial_save = self.household_save.copy()
        initial_capital = self.household_capital.copy()
        initial_consumption = self.household_consumption.copy()
        initial_total_capital = self.total_capital

        # Update the households
        income = (w * self.Labour/self.N + r * self.household_capital)*self.dt
        savings = income * self.household_save
        change_cap = savings - self.dep*self.household_capital *self.dt
        self.household_capital = self.household_capital + change_cap
        self.household_consumption = income - savings

        change_total_cap = change_cap.sum()

        # Find who updates their savings
        test_figures = self.seed.random(self.N)
        updates = test_figures < self.dt/self.update_freq

        rows = np.where(updates)[0]

        if(rows.size > 0):
            
            # Matrix of neighbor consumption
            neighbor_consumption = self.neighbors[rows] * self.household_consumption
            # Vector of maximum neighbor consumption indexes
            max_neighbor_consumption = neighbor_consumption.argmax(axis = 1)
    
            # Vector of raw savings updates
            raw_savings = self.household_save[max_neighbor_consumption]
            old_savings = self.household_save[rows]
            
            change_rate = raw_savings != old_savings
            
            # Add in noise & Clip
            raw_savings_2 = (1-change_rate)*old_savings + change_rate * np.clip(raw_savings + self.seed.uniform(-0.01,0.01, rows.size), 0,1)

            self.household_save[rows] = raw_savings_2

        self.total_capital += change_total_cap

        # update the history
        
        self.tick += 1
        if self.tick % self.update_every == 0:
            self.save_history.append(initial_save)
            self.capital_history.append(initial_capital)
            self.consumption_history.append(initial_consumption)
            self.total_capital_history.append(initial_total_capital)

