import numpy as np
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value

airports = ["ATL", "ORD", "DEN", "IAH", "LAX", "MIA", "JFK", "SFO", "SEA", "DCA"]
# Define the cost matrix (c[i][j])
cost_matrix = np.array([
    [0, 587, 1212, 701, 1936, 604, 748, 2139, 2182, 543],
    [587, 0, 920, 940, 1745, 1188, 713, 1858, 1737, 597],
    [1212, 920, 0, 879, 831, 1726, 1631, 949, 1021, 1494],
    [701, 940, 879, 0, 1379, 968, 1420, 1645, 1891, 1220],
    [1936, 1745, 831, 1379, 0, 2339, 2451, 347, 959, 2300],
    [604, 1188, 1726, 968, 2339, 0, 1092, 2594, 2734, 923],
    [748, 713, 1631, 1420, 2451, 1092, 0, 2571, 2408, 205],
    [2139, 1858, 949, 1645, 347, 2594, 2571, 0, 678, 2442],
    [2182, 1737, 1021, 1891, 959, 2734, 2408, 678, 0, 2329],
    [543, 597, 1494, 1220, 2300, 923, 205, 2442, 2329, 0]
])

# List of cities (0 to N-1)
cities = list(range(len(cost_matrix)))
N = len(cities)

# Create the problem
model = LpProblem("TSP_MTZ", LpMinimize)

# Define variables
x = LpVariable.dicts("x", [(i, j) for i in cities for j in cities], 0, 1, cat="Binary")  # Binary decision variable
u = LpVariable.dicts("u", cities, 0, N-1, cat="Continuous")  # Auxiliary MTZ variables

# Objective: Minimize total cost
model += lpSum(x[i, j] * cost_matrix[i][j] for i in cities for j in cities)

# Constraints
# Each city has exactly one edge going out
for j in cities:
    model += lpSum(x[i, j] for i in cities if i != j) == 1, f"Out_{j}"

# Each city has exactly one edge coming in
for i in cities:
    model += lpSum(x[i, j] for j in cities if i != j) == 1, f"In_{i}"

# No self-loops
for i in cities:
    model += x[i, i] == 0, f"NoSelfLoop_{i}"

# MTZ Constraints
for i in cities:
    for j in cities[1:]:  # Skip the first city (arbitrary root)
        if i != j:
            model += u[i] - u[j] + N * x[i, j] <= N - 1, f"MTZ_{i}_{j}"

# Solve the problem
model.solve()

# Retrieve the solution
solution_matrix = np.zeros((N, N), dtype=int)
for (i, j) in x:
    solution_matrix[i, j] = int(value(x[i, j]))

# Extract subtours
def find_subtours(sol):
    visited = [False] * N
    subtours = []

    for start in range(N):
        if not visited[start]:
            current = start
            subtour = []
            while not visited[current]:
                subtour.append(airports[current])  # Append the city name
                visited[current] = True
                # Find the next city in the tour
                current = next(j for j in range(N) if sol[current, j] == 1)
            subtours.append(subtour)
    return subtours

# Display results
subtours = find_subtours(solution_matrix)
print("Tour length:", value(model.objective))
print("Subtours:", subtours)
print("Solution Matrix:")
print(solution_matrix)
# returns different solution but same amount of miles traveled so I'd say its pretty good route
