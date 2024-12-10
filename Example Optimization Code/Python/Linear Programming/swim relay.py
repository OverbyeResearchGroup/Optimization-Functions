# functions to solve
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value
import numpy as np
from tabulate import tabulate

# Define strokes and names
strokes = ['backstroke', 'breaststroke', 'butterfly', 'freestyle']
names = ['Carl', 'Chris', 'David', 'Tony', 'Ken']

# Define raw times data
raw = np.array([
    [37.7, 32.9, 33.8, 37.0, 35.4],
    [43.4, 33.1, 42.2, 34.7, 41.8],
    [33.3, 28.5, 38.9, 30.4, 33.6],
    [29.2, 26.4, 29.6, 28.5, 31.1]
])

# Create the model
model = LpProblem("Swim_Optimization", LpMinimize)

# Create variables
x = LpVariable.dicts("x", (strokes, names), 0, 1, cat='Binary')

# Add constraints
# Each swimmer swims at most one event
for j in names:
    model += lpSum(x[i][j] for i in strokes) <= 1

# Each event has exactly one swimmer
for i in strokes:
    model += lpSum(x[i][j] for j in names) == 1

# Objective function: minimize total time
model += lpSum(x[i][j] * raw[strokes.index(i)][names.index(j)] for i in strokes for j in names)

# Solve the problem
model.solve()

# Extract results
assignment = np.zeros((len(strokes), len(names)))
for i in strokes:
    for j in names:
        assignment[strokes.index(i), names.index(j)] = value(x[i][j])

# Print results
# Assuming `strokes` is a list of strokes and `names` is a list of swimmer names.
# `assignment` is a 2D array or list where `assignment[i][j]` indicates assignment

# Prepare the header
header = ["Stroke \ Name"] + names

# Prepare the rows
rows = []
for i, stroke in enumerate(strokes):
    row = [stroke] + [f"{assignment[i][j]:.0f}" for j in range(len(names))]
    rows.append(row)

# Print the formatted table
print("Assignment matrix:")
print(tabulate(rows, headers=header, tablefmt="grid"))
