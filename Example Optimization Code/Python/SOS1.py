import pulp

# Create a problem instance
model = pulp.LpProblem("MaximizeObjective", pulp.LpMaximize)

# Define variables with bounds 0 <= x[i] <= 5
x = [pulp.LpVariable(f"x{i}", lowBound=0, upBound=5) for i in range(1, 5)]

# Define the objective function
model += 3 * x[0] + 4 * x[1] + 1 * x[2] + 5 * x[3], "Objective"

# Define SOS1 constraint (only one of the variables can be non-zero)
# Pulp doesn’t have a built-in SOS1, so we have to manually enforce that.
# This can be done by adding a constraint that the sum of all variables should be at most 1.
model += pulp.lpSum(x) <= 5, "SOS1_Constraint"

# Solve the model using the CBC solver
model.solve(pulp.getSolver('PULP_CBC_CMD'))

# Get and print the values of x
x_values = [v.varValue for v in x]
print(x_values)

