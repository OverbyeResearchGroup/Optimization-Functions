import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO

# Parameters
n = 6
pi = np.pi

# Create a model
m = GEKKO(remote=False)

# Variables
r = [m.Var(value=1, lb=0, ub=1) for i in range(n)]  # radius variables
theta = [m.Var(value=0, lb=0, ub=2*pi) for i in range(n)]  # angle variables

# Constraints
theta[0].value = 0  # theta[1] == 0
for i in range(n-1):
    m.Equation(theta[i+1] >= theta[i])  # impose order on angles

# Objective function
obj = 0.5 * sum([r[i] * r[i+1] * m.sin(theta[i+1] - theta[i]) for i in range(n-1)]) + 0.5 * r[0] * r[n-1] * m.sin(theta[0] - theta[n-1])

m.Maximize(obj)

# Solve the model
m.solve(disp=False)

# Get results
r_opt = np.array([r[i].value[0] for i in range(n)])
theta_opt = np.array([theta[i].value[0] for i in range(n)])

# Print optimal area
optimal_area = 0.5 * sum(r_opt[i] * r_opt[i+1] * np.sin(theta_opt[i+1] - theta_opt[i]) for i in range(n-1)) + 0.5 * r_opt[0] * r_opt[n-1] * np.sin(theta_opt[0] - theta_opt[n-1])
print("Optimal area:", optimal_area)

# Plot
t = np.linspace(0, 2*pi, 100)
plt.figure(figsize=(5, 5))

# Plot unit circle
plt.plot(np.cos(t), np.sin(t), "b-")

# Plot optimal shape
ropt = np.append(r_opt, r_opt[0])  # r[1] to r[n], and r[1] again
topt = np.append(theta_opt, theta_opt[0])  # theta[1] to theta[n], and theta[1] again
plt.plot(ropt * np.cos(topt), ropt * np.sin(topt), "r.-")

# Final touches on the plot
plt.axis("equal")
plt.axis("off")
plt.tight_layout()
plt.show()
