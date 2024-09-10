# Problem Data
# types of trophies produced
sports = ["football", "soccer"]

# wood required for each type of trophy (in board feet)
wood = {"football": 4, "soccer": 2}

# plaques required for each type of trophy
plaques = {"football": 1, "soccer": 1}

# profit made for each trophy
profit = {"football": 12, "soccer": 9}

# quantities in stock for each ingredient
num_wood = 4800
num_plaques = 1750
num_football = 1000
num_soccer = 1500

#Problem Solver
from pulp import *

# Create a problem instance
m = LpProblem("Maximize_Profit", LpMaximize)

# Decision variables for the number of trophies
trophies = {sport: LpVariable(f"trophies_{sport}", lowBound=0, cat='Integer') for sport in sports}

# Objective function: total profit
tot_profit = lpSum([trophies[sport] * profit[sport] for sport in sports])

# Constraints
m += trophies["soccer"] <= num_soccer  # Maximum number of soccer balls
m += trophies["football"] <= num_football  # Maximum number of footballs

# Total plaques constraint
tot_plaques = lpSum([trophies[sport] * plaques[sport] for sport in sports])
m += tot_plaques <= num_plaques  # Maximum number of plaques

# Total wood constraint
tot_wood = lpSum([trophies[sport] * wood[sport] for sport in sports])
m += tot_wood <= num_wood  # Maximum amount of wood

# Add the objective function to the model
m += tot_profit

# Solve the problem
m.solve()

# Print the results
for sport in sports:
    print(f"Number of {sport} trophies: {trophies[sport].varValue}")

print(f"Total profit will be: ${value(tot_profit)}")
print(f"Total wood used is {value(tot_wood)} board feet")
print(f"Total number of plaques used is {value(tot_plaques)}")
