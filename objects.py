import numpy as np

rng = np.random.default_rng()

class Household:
    def __init__(self, save, capital, consumption):
        self.save = save
        self.capital = capital
        self.consumption = consumption

class economy:

    """
    An economy

    Attrributes:
        N: the number of agents in the economy
        Labour: the total amount of labour in the economy.  Each agent provides a uniform Labour/N quantity
        neighbors: an adjacency matrix of neighbors.  Neighbors[i] gives you i's neighbors
        total_capital: the amount of capital in the economy.  Initially agents have one unit each
        alpha: the capital share of production
        dep: the rate at which capital depreciates
        dt: how much real time passes per tick.  dt -> 0, economy becomes continuous

    """
    def __init__(self, N, Labour, neighbors, update_freq, alpha, dep, dt):
        self.N = N
        self.Labour = Labour
        self.neighbors = neighbors
        

        self.households = np.array(N)
        
        
        self.households = []
        for i in range(N):
            save_rate = rng.uniform(0,1)
            self.households.append(Household(save_rate, 1, 0))

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
        self.record_every = 100


    def next_period(self):
        r = self.alpha * self.total_capital ** (self.alpha -1) * self.Labour **(1-self.alpha)
        w = (1-self.alpha) * self.total_capital ** (self.alpha) * self.Labour **(-self.alpha)

        change_total_cap = 0

        initial_save = []
        initial_capital = []
        initial_consumption = []

        for i in range(self.N):
            
            household = self.households[i]
            
            income = (w * self.Labour/self.N + r * household.capital)*self.dt
            savings = income * household.save
            change_cap = savings - self.dep*household.capital *self.dt
            household.capital = household.capital + change_cap
            
            change_total_cap += change_cap
            household.consumption = income - savings

            initial_save.append(household.save)
            initial_capital.append(household.capital)
            initial_consumption.append(household.consumption)

        new_savings_rate = []
        for i in range(self.N):
            new_savings_rate.append(self.households[i].save)

        
        for i in range(self.N):
            # update saving rate - consume and then compare
            household = self.households[i]
            
            if(rng.random() < self.dt/self.update_freq):
                # find maximum savings rate
                highest_consump_neighbor = i
                household_neighbors = self.neighbors[i]
                for j in range(self.N):
                    if household_neighbors[j] == 1:
                        if(self.households[j].consumption > self.households[highest_consump_neighbor].consumption):
                            highest_consump_neighbor = j
                if(highest_consump_neighbor != i):
                    new_savings_rate[i] = np.clip(self.households[highest_consump_neighbor].save + rng.uniform(-0.01, 0.01), 0,1)


            self.households[i] = household

        self.total_capital += change_total_cap

        # update the savings rate
        for i in range(self.N):
            self.households[i].save = new_savings_rate[i]

        # update the history
        self.tick += 1
        if self.tick % self.record_every == 0:
            self.save_history.append(initial_save)
            self.capital_history.append(initial_capital)
            self.consumption_history.append(initial_consumption)
            self.total_capital_history.append(self.total_capital)

