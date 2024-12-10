from gekko import GEKKO

# Create a GEKKO model
m = GEKKO(remote=False)

# Define the variables
r = m.Var(value=25, lb=25, ub=60)  # Initial value, lower bound, upper bound
h = m.Var(value=0, lb=0)           # Initial value, lower bound
c = m.Var(value=50, lb=50)         # Initial value, lower bound

# Define the constraints
m.Equation(r + h + c == 100)  # Sum constraint

# Nonlinear constraints
m.Equation(12.5 - 0.1 * h - 0.001 * h**2 >= 12)  # Tensile constraint
m.Equation(17 + 0.35 * r - 0.04 * h - 0.002 * r**2 >= 16)  # Elasticity constraint
m.Equation(25 <= 34 + 0.1 * r + 0.06 * h - 0.3 * c +
           0.01 * r * h + 0.005 * h**2 + 0.001 * c**1.95)  # Hardness lower bound
m.Equation(34 + 0.1 * r + 0.06 * h - 0.3 * c +
           0.01 * r * h + 0.005 * h**2 + 0.001 * c**1.95 <= 35)  # Hardness upper bound

# Define the objective function
m.Obj(0.04 * r + 0.01 * h + 0.07 * c)  # Minimize cost

# Solve the optimization problem
m.solve(disp=False)  # Set disp=True for solver output

# Display results
print(f"Optimal values:")
print(f"r (rubber) = {r.value[0]:.4f}")
print(f"h (oil)    = {h.value[0]:.4f}")
print(f"c (carbon) = {c.value[0]:.4f}")
