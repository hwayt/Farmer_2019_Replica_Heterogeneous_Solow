import numpy as np

rng = np.random.default_rng()

class economy:

    """
    An economy

    Attrributes:
        N: the number of agents in the economy
        Labour: the total amount of labour in the economy.  Each agent provides a uniform Labour/N quantity
        neighbors: an adjacency matrix of neighbors.  Neighbors[i] gives you i's neighbors. You are always your own neighbor
        total_capital: the amount of capital in the economy.  Initially agents have one unit each
        alpha: the capital share of production
        dep: the rate at which capital depreciates
        dt: how much real time passes per tick.  dt -> 0, economy becomes continuous

    """
    def __init__(self, N, Labour, neighbors, update_freq, alpha, dep, dt):
        self.N = N
        self.Labour = Labour
        self.neighbors = neighbors
        self.total_capital = N
        self.update_freq = update_freq
        self.alpha = alpha
        self.dep = dep
        self.dt = dt

        self.save_history = []
        self.capital_history = []
        self.consumption_history = []
        self.total_capital_history = []
        self.tick = 0
        self.update_every = int(round(1/dt))
        

        # Set up numpy arrays for the households
        self.household_save = rng.uniform(0,1,size=self.N)
        self.household_capital = np.ones(self.N)
        self.household_consumption = np.zeros(self.N)



    def next_period(self):
        r = self.alpha * self.total_capital ** (self.alpha -1) * self.Labour **(1-self.alpha)
        w = (1-self.alpha) * self.total_capital ** (self.alpha) * self.Labour **(-self.alpha)

        initial_save = self.household_save
        initial_capital = self.household_capital
        initial_consumption = self.household_consumption
        initial_total_capital = self.total_capital

        # Update the households
        income = (w * self.Labour/self.N + r * self.household_capital)*self.dt
        savings = income * self.household_save
        change_cap = savings - self.dep*self.household_capital *self.dt
        self.household_capital = self.household_capital + change_cap
        self.household_consumption = income - savings

        change_total_cap = change_cap.sum()

        # Store old saving rate
        old_saving_rate = self.household_save

        # Find who updates their savings
        test_figures = rng.random(self.N)
        updates = test_figures < self.dt/self.update_freq


        # Matrix of neighbor consumption
        neighbor_consumption = self.neighbors * self.household_consumption
        # Vector of maximum neighbor consumption indexes
        max_neighbor_consumption = neighbor_consumption.argmax(axis = 1)

        # Vector of raw savings updates
        raw_savings = self.household_save[max_neighbor_consumption]

        # Vector of raw savings updates only updated when possible
        raw_savings_2 = (1-updates)*old_saving_rate + updates * raw_savings

        # Figure out which have been updated
        updates_2 = raw_savings_2 != old_saving_rate

        # Add in noise & Clip
        self.household_save = np.clip(raw_savings_2 + updates_2 * rnd.uniform(-0.01,0.01, self.N), 0,1)

        self.total_capital += change_total_cap

        # update the history
        
        self.tick += 1
        if self.tick % self.update_every == 0:
            self.save_history.append(initial_save)
            self.capital_history.append(initial_capital)
            self.consumption_history.append(initial_consumption)
            self.total_capital_history.append(initial_total_capital)

