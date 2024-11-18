import pulp

# Create a problem instance
model = pulp.LpProblem("MaximizeObjective", pulp.LpMaximize)

# Define variables
x = [pulp.LpVariable(f"x{i}", lowBound=0, upBound=5) for i in range(1, 5)]
z = [pulp.LpVariable(f"z{i}", lowBound=0) for i in range(1, 4)]  # z[i] >= 0

# Define the objective function
model += 3 * x[0] + 4 * x[1] + 1 * x[2] + 5 * x[3], "Objective"

# Constraint: sum of z[i] == 1 (exactly one z[i] is non-zero)
model += pulp.lpSum(z) == 1, "BinaryConstraint"

# Constraints based on the relationship between x[i] and z[i]
model += x[0] <= 5 * z[0], "Constraint_x1"
model += x[1] <= 5 * z[0] + 5 * z[1], "Constraint_x2"
model += x[2] <= 5 * z[1] + 5 * z[2], "Constraint_x3"
model += x[3] <= 5 * z[2], "Constraint_x4"

# Solve the model using the CBC solver
model.solve(pulp.getSolver('PULP_CBC_CMD'))

# Get and print the values of x
x_values = [x[i].varValue for i in range(4)]
print("Values of x:", x_values)
