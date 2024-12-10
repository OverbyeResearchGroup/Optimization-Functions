from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

# Define the model
model = LpProblem(name="clothing-optimization", sense=LpMaximize)

# Define continuous variables x and binary variables z
x = {i: LpVariable(f"x_{i}", lowBound=0, cat="Continuous") for i in range(1, 4)}
z = {i: LpVariable(f"z_{i}", cat="Binary") for i in range(1, 4)}

# Define the constraints
model += (3 * x[1] + 2 * x[2] + 6 * x[3] <= 150), "labor_budget"
model += (4 * x[1] + 3 * x[2] + 4 * x[3] <= 160), "cloth_budget"
for i in range(1, 4):
    model += (x[i] <= 50 * z[i]), f"x_z_constraint_{i}"  # if x[i] > 0 then z[i] = 1

# Define the objective
model += lpSum([6 * x[1], 4 * x[2], 7 * x[3], -200 * z[1], -150 * z[2], -100 * z[3]]), "net_profit"

# Solve the model
status = model.solve(PULP_CBC_CMD(msg=0))

# Display results
print(f"Solution Status: {model.status}")
print(f"{x[1].value()} shirts")
print(f"{x[2].value()} shorts")
print(f"{x[3].value()} pants")
print(f"${model.objective.value()} of net profit")
