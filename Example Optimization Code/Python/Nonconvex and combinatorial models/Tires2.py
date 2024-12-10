from gekko import GEKKO

# Constants
ph = 0.05
pr = 0.1
pc = 0.02

# Initialize the GEKKO model
m = GEKKO(remote=False)

# Define the variables
h = m.Var(value=0, lb=0, ub=4.77)  # h: oil
c = m.Var(value=50, lb=50)         # c: carbon

# Define the constraints
m.Equation(50 <= h + c)  # Lower bound constraint
m.Equation(h + c <= 75)  # Upper bound constraint

# Nonlinear constraints
m.Equation(32 + 0.05 * c - 0.002 * c**2 + 0.01 * h - 0.004 * c * h - 0.002 * h**2 >= 16)  # Elasticity
m.Equation(25 <= 44 + 0.96 * h - 0.4 * c - 0.01 * c * h + 0.005 * h**2 + 0.001 * c**1.95)  # Hardness lower bound
m.Equation(44 + 0.96 * h - 0.4 * c - 0.01 * c * h + 0.005 * h**2 + 0.001 * c**1.95 <= 35)  # Hardness upper bound

# Define the objective function
m.Obj((ph - pr) * h + (pc - pr) * c)  # Minimize cost

# Solve the optimization problem
m.solve(disp=False)  # Set disp=True for solver output

# Display results
print(f"Optimal values:")
print(f"100 - h - c (rubber) = {100 - h.value[0] - c.value[0]:.4f}")
print(f"h (oil)              = {h.value[0]:.4f}")
print(f"c (carbon)           = {c.value[0]:.4f}")
