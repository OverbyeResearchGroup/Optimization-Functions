import pulp

# Create a problem instance
model = pulp.LpProblem("MaximizeObjective", pulp.LpMaximize)

# Define the variables for x[i] between 0 and 5
x = [pulp.LpVariable(f"x{i}", lowBound=0, upBound=5) for i in range(1, 5)]

# Define binary indicator variables for each x[i] (1 if x[i] is non-zero)
y = [pulp.LpVariable(f"y{i}", cat="Binary") for i in range(1, 5)]

# Define the objective function: Maximize 3x[1] + 4x[2] + 1x[3] + 5x[4]
model += 3 * x[0] + 4 * x[1] + 1 * x[2] + 5 * x[3], "Objective"

# Add constraint to ensure that only two x[i]'s are non-zero
for i in range(4):
    model += x[i] <= 5 * y[i], f"Link_{i+1}"  # If y[i] = 0, x[i] must be 0

# Constraint: Sum of the binary variables y[i] must be exactly 2 (exactly two x[i] are non-zero)
model += pulp.lpSum(y) == 2, "SOS2Constraint"

# Solve the model using the CBC solver
model.solve(pulp.getSolver('PULP_CBC_CMD'))

# Get and print the values of x
x_values = [x[i].varValue for i in range(4)]
print("Values of x:", x_values)
