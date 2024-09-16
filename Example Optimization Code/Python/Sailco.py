from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value

# Monthly demand for boats
d = [40, 60, 70, 25]

# Create the model
model = LpProblem("Boat_Production", LpMinimize)

# Create variables
x = [LpVariable(f"x_{i+1}", lowBound=0, upBound=40) for i in range(4)]  # boats produced with regular labor
y = [LpVariable(f"y_{i+1}", lowBound=0) for i in range(4)]              # boats produced with overtime labor
h = [LpVariable(f"h_{i+1}", lowBound=0) for i in range(5)]              # boats held in inventory

# Add constraints
model += h[0] == 10
for i in range(4):
    model += h[i] + x[i] + y[i] == d[i] + h[i+1]  # conservation of boats

# Objective function: minimize costs
model += 400 * lpSum(x) + 450 * lpSum(y) + 20 * lpSum(h)

# Solve the problem
model.solve()

# Print the results
x_values = [int(value(var)) for var in x]
y_values = [int(value(var)) for var in y]
h_values = [int(value(var)) for var in h]

print("Build", x_values, "using regular labor")
print("Build", y_values, "using overtime labor")
print("Inventory:", h_values)
