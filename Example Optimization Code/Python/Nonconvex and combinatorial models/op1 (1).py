from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

# Define the model
model = LpProblem("Trophy_Profit_Maximization", LpMaximize)

# Define the variables
f = LpVariable('football_trophies', lowBound=0, upBound=1000)
s = LpVariable('soccer_trophies', lowBound=0, upBound=1500)

# Define the constraints
model += 4*f + 2*s <= 4800  # total board feet of wood
model += f + s <= 1750      # total number of plaques

# Define the objective
model += 12*f + 9*s         # maximize profit

# Solve the model
status = model.solve()

# Print the results
print(f"Status: {status}")
print(f"Build {value(f)} football trophies.")
print(f"Build {value(s)} soccer trophies.")
print(f"Total profit will be ${value(model.objective)}")
