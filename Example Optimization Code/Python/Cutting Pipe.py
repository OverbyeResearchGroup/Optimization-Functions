from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpInteger, LpBinary, PULP_CBC_CMD

# Scaling factor
scale = 1

# Upper bound on the number of pipes needed
N = 16 * scale

# Create the problem
model = LpProblem("Minimize_Pipes", LpMinimize)

# Variables
x = LpVariable.dicts("x", ((i, j) for i in range(1, 4) for j in range(1, N + 1)), lowBound=0, cat=LpInteger)
z = LpVariable.dicts("z", (j for j in range(1, N + 1)), cat=LpBinary)

# Constraints
for j in range(1, N + 1):
    model += 4 * x[1, j] + 5 * x[2, j] + 6 * x[3, j] <= 19, f"Capacity_Constraint_{j}"

model += lpSum(x[1, j] for j in range(1, N + 1)) >= 12 * scale, "Demand_1"
model += lpSum(x[2, j] for j in range(1, N + 1)) >= 15 * scale, "Demand_2"
model += lpSum(x[3, j] for j in range(1, N + 1)) >= 22 * scale, "Demand_3"

for j in range(1, N + 1):
    model += x[1, j] <= 4 * z[j], f"x1_bound_{j}"
    model += x[2, j] <= 3 * z[j], f"x2_bound_{j}"
    model += x[3, j] <= 3 * z[j], f"x3_bound_{j}"

# Symmetry-breaking constraints
for j in range(1, N):
    model += z[j] >= z[j + 1], f"Symmetry_Breaking_{j}"

# Objective function
model += lpSum(z[j] for j in range(1, N + 1)), "Minimize_Number_of_Pipes"

# Solve the model
solver = PULP_CBC_CMD(msg=True)  # Use default CBC solver
model.solve(solver)

# Display results
print("Status:", model.status)
print("Objective value (min z):", model.objective.value())
for j in range(1, N + 1):
    print(f"z[{j}] = {z[j].value()}")
    for i in range(1, 4):
        print(f"x[{i},{j}] = {x[i, j].value()}")
