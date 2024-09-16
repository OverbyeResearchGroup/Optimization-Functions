from pulp import LpProblem, LpVariable, LpMinimize, value, LpStatus

# Define the problem
m = LpProblem("Minimize Cost", LpMinimize)

# Define the variables with bounds
lambda_vars = [LpVariable(f'λ{i + 1}', lowBound=0) for i in range(4)]

# Define the constraints
m += 4 * lambda_vars[0] + lambda_vars[1] + lambda_vars[2] >= 12
m += 2 * lambda_vars[0] + lambda_vars[1] + lambda_vars[3] >= 9

# Define the objective function
m += 4800 * lambda_vars[0] + 1750 * lambda_vars[1] + 1000 * lambda_vars[2] + 1500 * lambda_vars[3]

# Solve the problem
status = m.solve()

# Display the status
print("Status:", LpStatus[status])

# Get the values of the variables
lambda_values = [value(var) for var in lambda_vars]
print("Dual variables are:", lambda_values)

# Get the optimal objective value
print("Optimal objective is:", value(m.objective))
