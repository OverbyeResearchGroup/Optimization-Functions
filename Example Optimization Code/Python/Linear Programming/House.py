from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value

# Task names
tasks = [chr(i) for i in range(ord('a'), ord('x') + 1)]

# Project durations
dur = [0, 4, 2, 4, 6, 1, 2, 3, 2, 4, 10, 3, 1, 2, 3, 2, 1, 1, 2, 3, 1, 2, 5, 0]
duration = dict(zip(tasks, dur))

# Project dependencies (ancestors)
pre = {
    'a': [], 'b': ['a'], 'c': ['b'], 'd': ['c'], 'e': ['d'], 'f': ['c'], 'g': ['f'], 'h': ['f'],
    'i': ['d'], 'j': ['d', 'g'], 'k': ['i', 'j', 'h'], 'l': ['k'], 'm': ['l'], 'n': ['l'],
    'o': ['l'], 'p': ['e'], 'q': ['p'], 'r': ['c'], 's': ['o', 't'], 't': ['m', 'n'],
    'u': ['t'], 'v': ['q', 'r'], 'w': ['v'], 'x': ['s', 'u', 'w']
}

# Create the model
model = LpProblem("Project_Scheduling", LpMinimize)

# Create variables
tstart = {task: LpVariable(f"tstart_{task}", lowBound=0) for task in tasks}

# Add constraints
for i in tasks:
    for j in pre[i]:
        model += tstart[i] >= tstart[j] + duration[j]

# Set the start time of the first task
model += tstart['a'] == 0

# Objective function: minimize the total duration
model += tstart['x'] + duration['x']

# Solve the problem
model.solve()

# Print the results
tstart_values = {task: value(tstart[task]) for task in tasks}
print(tstart_values)
print("Minimum duration:", value(model.objective))
