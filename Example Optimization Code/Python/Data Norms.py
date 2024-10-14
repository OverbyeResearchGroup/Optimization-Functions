import cvxpy as cp
import numpy as np

# Set the random seed for reproducibility
np.random.seed(0)

# Define the number of random values
N = 9

# Generate N random numbers, scale them by 10, and sort the result
y = np.sort(10 * np.random.rand(N))

print(y)

# Define the variable
x = cp.Variable()

# Define the objective function: minimize the 2-norm
objective = cp.Minimize(cp.sum_squares(y - x)**2)

# Create the problem
problem = cp.Problem(objective)

# Solve the problem using Gurobi
problem.solve(solver=cp.GUROBI, verbose=True)
average = np.average(y)
# Print the optimal x value
print(f"The optimal x value is: {x.value}")
print(average)
