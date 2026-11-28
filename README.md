For the interest of full understanding, this project has been completed with minimal AI input (debugging only). This project is not meant to be cutting edge.

# Heterogeneous-Agent Solow Model

A replication (and simplification) of "Emergent inequality and business cycles in a simple behavioral macroeonomic model" by Asano, Kolb, Heitzig and Farmer, 2021.

## Method
We take N heterogeneous agents, distinguished by their savings rate. Standard Solow model set up is used, with a fixed initial level of capital owned by each agent, a fixed depreciation rate, capital share of income etc. We initialise with agents with savings rate distributed evenly between 0 and 2*alpha, so the average rate is the golden rule level alpha (this helps prevent initial dramatic oscillations).

As in Asano et al, agents are modelled as myopic; each period, they interact with their neighbors with some fixed probability.  If they interact with their neighbors, they update their savings rate to that of their highest consumption neighbor.

## Key Results
I replicated the paper's core result

Short tau (regular interactions) leads to a stable poverty trap.  Fluctuations shrink with noise
Long tau (irregular interactions) leads to sustained cycles (the unstable regime) around the golden rule level.  Even with noise removed, instability may continue for extended time period.
