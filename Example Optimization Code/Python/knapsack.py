from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

w = [12, 2, 4, 1, 1]  # weights
v = [4, 2, 10, 2, 1]  # values
W = 15
n = len(w)

# Define the model
model = LpProblem(name="binary-optimization", sense=LpMaximize)

# Define binary variables
z = {i: LpVariable(name=f"z_{i}", cat="Binary") for i in range(1, 6)}

# Define the constraint
model += (12 * z[1] + 2 * z[2] + 4 * z[3] + z[4] + z[5] <= 15), "constraint"

# Define the objective
model += lpSum([4 * z[1], 2 * z[2], 10 * z[3], 2 * z[4], 1 * z[5]]), "objective"

# Solve the model
status = model.solve(PULP_CBC_CMD(msg=0))

# Display results
print("Status:", model.status)
print("z =", {i: z[i].value() for i in z})
print("Objective =", model.objective.value())
