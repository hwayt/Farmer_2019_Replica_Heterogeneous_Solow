import random
import numpy as np

rng = np.random.default_rng()

class household:
    def __init__(self, save, capital, consumption):
        self.save = save
        self.capital = capital
        self.consumption = consuption

class economy

    """
    An economy

    Attrributes:
        N: the number of agents in the economy
        Labour: the total amount of labour in the economy.  Each agent provides a uniform Labour/N quantit
        neighbors: an adjacency matrix of neighbors.  Neighbors[i] gives you i's neighbors
        total_capital: the amount of capital in the economy.  Initially agents have one unit each
        alpha: the capital share of production
        dep: the rate at chich capital depreciates
        dt: how much real time passes per tick.  dt -> 0, economy becomes continuous

    """
    def __init__(self, N, Labour, neighbors, total_capital, update_freq, alpha, dep, dt):
        self.N = N
        self.Labour = Labour
        self.neighbors = neighbors
        

        households = []
        for i in range(N):
            save_rate = random.uniform(0,1)
            households.append(household(save_rate, 1, 0)

        self.total_capital = N
        self.update_freq = update_freq
        self.dep = dep
        self.dt = dt


    def next_period
        r = alpha * total_capital ^^ (alpha -1) * Labour **(1-alpha)
        w = (1-alpha) * total_capital ^^ (alpha) * Labour **(-alpha)

        change_total_cap = 0

        for i in range(N):
            household = households[i]
            income = (w * Labour/N + r * household.capital)*dt
            savings = income * save
            change_cap = savings - dep*household.capital *dt
            household.capital = household.capital + change_cap
            
            change_total_cap += change_cap
            household.consumption = income - savings

        for i in range(N):
            # update saving rate - consume and then compare
            household = households[i]
            
            if(rng.random()/dt < update_freq):
                # find maximum savings rate
                highest_consump_neighbor = i
                household_neighbors = neighbors[i]
                highest_consump_neighbor = i
                for j in range[N]
                    if[household_neighbors[j] = 1:
                        if(self.households[j].consumption > self.households[highest_consump_neighbor].consumption):
                            highest_consump_neighbor = j
                if(highest_consump_neighbor != i):
                    household.save = self.households[j].save + random.uniform(-0.01, 0.01)

            households[i] = household

        self.total_capital += change_total_cap

            
            