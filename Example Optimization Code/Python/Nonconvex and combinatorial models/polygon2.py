import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO

# Parameters
n = 6

# Create a model
m = GEKKO(remote=False)

# Variables for coordinates (x, y)
x = [m.Var(value=np.random.rand(), lb=-1, ub=1) for i in range(n)]
y = [m.Var(value=np.random.rand(), lb=-1, ub=1) for i in range(n)]

# Constraints for unit circle (x^2 + y^2 <= 1)
for i in range(n):
    m.Equation(x[i]**2 + y[i]**2 <= 1)

# Add ordering constraints to the vertices
for i in range(n-1):
    m.Equation(x[i]*y[i+1] - y[i]*x[i+1] >= 0)

m.Equation(x[n-1]*y[0] - y[n-1]*x[0] >= 0)

# Objective function
obj = 0.5 * sum([x[i]*y[i+1] - y[i]*x[i+1] for i in range(n-1)]) + 0.5 * (x[n-1]*y[0] - y[n-1]*x[0])

# Maximize the objective function
m.Maximize(obj)

# Solve the model using IPOPT solver
m.options.SOLVER = 3  # IPOPT solver
m.solve(disp=True)

# Get optimal values of x and y
x_opt = np.array([x[i].value[0] for i in range(n)] + [x[0].value[0]])  # Close the loop by adding x[0] to x_opt
y_opt = np.array([y[i].value[0] for i in range(n)] + [y[0].value[0]])  # Same for y_opt

# Print optimal area (objective function value)
optimal_area = 0.5 * sum(x_opt[i] * y_opt[i+1] - y_opt[i] * x_opt[i+1] for i in range(n-1)) + 0.5 * (x_opt[n-1] * y_opt[0] - y_opt[n-1] * x_opt[0])
print("Optimal area:", optimal_area)

# Plot the result
t = np.linspace(0, 2*np.pi, 100)
plt.figure(figsize=(5, 5))

# Plot the unit circle
plt.plot(np.cos(t), np.sin(t), "b-")

# Plot the optimal shape
plt.plot(x_opt, y_opt, "r.-")

# Final touches on the plot
plt.axis("equal")
plt.axis("off")
plt.tight_layout()
plt.show()
