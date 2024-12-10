import cvxpy as cp
import numpy as np

# Assuming y is already defined, for example:
N = 9
np.random.seed(0)
y = np.sort(10 * np.random.rand(N))

# Define the variable
x = cp.Variable()

# Define the auxiliary variables for the 1-norm
t = cp.Variable(N)

# Define the constraints
constraints = [
    y - x <= t,
    -(y - x) <= t
]

objective = cp.Minimize(cp.sum(t))

problem = cp.Problem(objective, constraints)

problem.solve(solver=cp.GUROBI, verbose=True)
print(f"The optimal x value is: {x.value}")
median = np.median(y)
print(median)
