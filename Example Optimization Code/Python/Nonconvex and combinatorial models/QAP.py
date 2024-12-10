import numpy as np
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value

# Sets
stores = ["A", "B", "C", "D"]
locations = [1, 2, 3, 4]

# Flow matrix (f)
f = np.array([
    [0, 5, 2, 7],
    [5, 0, 3, 8],
    [2, 3, 0, 3],
    [7, 8, 3, 0]
])

# Distance matrix (d)
d = np.array([
    [0, 80, 150, 170],
    [80, 0, 130, 100],
    [150, 130, 0, 120],
    [170, 100, 120, 0]
])

# Problem definition
model = LpProblem("Facility_Location", LpMinimize)

# Decision variables
x = LpVariable.dicts("x", [(i, j) for i in stores for j in locations], 0, 1, cat="Binary")
z = LpVariable.dicts("z", [(i, j, k, l) for i in stores for j in locations for k in stores for l in locations], 0, 1, cat="Binary")

# Constraints
# Each store is assigned to exactly one location
for i in stores:
    model += lpSum(x[(i, j)] for j in locations) == 1, f"Store_Assignment_{i}"

# Each location is assigned to exactly one store
for j in locations:
    model += lpSum(x[(i, j)] for i in stores) == 1, f"Location_Assignment_{j}"

# Constraints linking x and z variables
for i in stores:
    for j in locations:
        for k in stores:
            for l in locations:
                model += x[(i, j)] >= z[(i, j, k, l)], f"Link_x_z_1_{i}_{j}_{k}_{l}"
                model += x[(k, l)] >= z[(i, j, k, l)], f"Link_x_z_2_{i}_{j}_{k}_{l}"
                model += x[(i, j)] + x[(k, l)] <= z[(i, j, k, l)] + 1, f"Link_x_z_3_{i}_{j}_{k}_{l}"

# Objective function
model += (1 / 2) * lpSum(f[stores.index(i)][stores.index(k)] * d[locations.index(j)][locations.index(l)] * z[(i, j, k, l)]
                         for i in stores for j in locations for k in stores for l in locations), "Total_Cost"

# Solve the problem
model.solve()

# Retrieve the solution
solution = np.zeros((len(stores), len(locations)), dtype=int)
for i in stores:
    for j in locations:
        solution[stores.index(i), locations.index(j)] = int(value(x[(i, j)]))

# Print the solution
print("Optimal Store-Location Assignment:")
print(solution)
