import cvxpy as cp
import numpy as np

# Define the matrix A and vector b
A = np.array([[2, -1, 2], [-1, 2, 4], [1, 2, -2], [-1, 0, 0], [0, -1, 0], [0, 0, -1]])
b = np.array([2, 16, 8, 0, 0, 0])

# Define the variables
r = cp.Variable(nonneg=True)  # radius
x = cp.Variable(3)  # coordinates of center

# Define the constraints
constraints = [A[i, :] @ x + r * np.linalg.norm(A[i, :]) <= b[i] for i in range(A.shape[0])]

# Define the objective
objective = cp.Maximize(r)  # maximize radius

# Define the problem
problem = cp.Problem(objective, constraints)

# Solve the problem
problem.solve()

# Get the results
center = x.value
radius = r.value

print("Status:", problem.status)
print("The coordinates of the Chebyshev center are:", center)
print("The largest possible radius is:", radius)
