from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value
import numpy as np

# Incidence matrix
A = np.array([
    [ 1,  1,  1,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  1,  1,  1,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  1,  1,  1],
    [-1,  0,  0, -1,  0,  0, -1,  0,  0],
    [ 0, -1,  0,  0, -1,  0,  0, -1,  0],
    [ 0,  0, -1,  0,  0, -1,  0,  0, -1]
])

# Supply and demand
b = [20, 30, 45, -30, -35, -30]

# Distances
c = [8, 15, 50, 10, 17, 20, 30, 26, 15]

# Create the model
model = LpProblem("Transportation_Problem", LpMinimize)

# Create variables
x = [LpVariable(f"x_{i+1}", lowBound=0) for i in range(9)]

# Add constraints
for i in range(6):
    model += lpSum(A[i][j] * x[j] for j in range(9)) == b[i]

# Objective function: minimize the cost
model += 4 * lpSum(c[i] * x[i] for i in range(9))

# Solve the problem
model.solve()

# Get the solution
xsol = [value(var) for var in x]
xsol_reshaped = np.reshape(xsol, (3, 3)).T

print(xsol_reshaped)
print("Total cost:", value(model.objective))