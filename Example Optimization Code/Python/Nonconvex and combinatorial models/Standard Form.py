from pulp import LpProblem, LpVariable, LpMinimize, LpStatus, value

# Create the model
model = LpProblem("Minimize_p_plus_q", LpMinimize)

# Define the variables
p = LpVariable("p")  # Unbounded variable
q = LpVariable("q", lowBound=1, upBound=4) # q is bounded between 1 and 4

# Add the objective function
model += p + q, "Objective"

# Add the constraints
model += 5 * p - 3 * q == 7, "Equality_Constraint"
model += 2 * p + q >= 2, "Inequality_Constraint"

# Solve the model
status = model.solve()

# Output the results
print("Status:", LpStatus[status])
print("p =", value(p))
print("q =", value(q))
print("Objective =", value(model.objective))
