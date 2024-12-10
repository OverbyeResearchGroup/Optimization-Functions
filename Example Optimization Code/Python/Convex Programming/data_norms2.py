import cvxpy as cp
import numpy as np
# Define the variables
x = cp.Variable()
r = cp.Variable()

y = [0.423017, 0.682693, 1.64566, 1.77329, 2.03477, 2.7888, 3.61828, 8.23648, 9.10357]


print(y)


# Define the constraints
constraints = [y - x <= r, -(y - x) <= r]

# Define the objective function (minimizing r)
objective = cp.Minimize(r)

# Formulate the problem
problem = cp.Problem(objective, constraints)

# Solve the problem
problem.solve()

# Output the optimal x value
print("The optimal x value is: ", x.value)

# Min calculates the midpoint from the end values while main calculates
# minimizes the largest difference between x and all y varabiles making solution more balanced

min = (y[0]+(len(y)-1))/2
print(min)