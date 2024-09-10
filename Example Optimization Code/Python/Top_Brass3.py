from collections import defaultdict

# The types of trophies produced
sports = ['football', 'soccer']

# Ingredients involved
ingredients = ['wood', 'plaque', 'brass_football', 'brass_soccer']

# Profits returned for each sport
profit = dict(zip(sports, [12, 9]))

# Quantities available for each ingredient
quant_avail = dict(zip(ingredients, [4800, 1750, 1000, 1500]))

# Recipes (how much of each ingredient is needed to produce each type of trophy)
recipe = defaultdict(dict)

# Filling in the recipe for each sport (trophy type)
# The rows correspond to sports and the columns to ingredients (wood, plaque, brass_football, brass_soccer)
recipe['football'] = {'wood': 4, 'plaque': 1, 'brass_football': 1, 'brass_soccer': 0}
recipe['soccer'] = {'wood': 2, 'plaque': 1, 'brass_football': 0, 'brass_soccer': 1}

# Example: Accessing information
print("Profit for each sport:", profit)
print("Quantities available:", quant_avail)
print("Recipe for football trophies:", recipe['football'])
print("Recipe for soccer trophies:", recipe['soccer'])

from pulp import *

# The types of trophies produced
sports = ['football', 'soccer']

# Ingredients involved
ingredients = ['wood', 'plaque', 'brass_football', 'brass_soccer']

# Profits returned for each sport
profit = {'football': 12, 'soccer': 9}

# Quantities available for each ingredient
quant_avail = {'wood': 4800, 'plaque': 1750, 'brass_football': 1000, 'brass_soccer': 1500}

# Recipe matrix (how much of each ingredient is needed to produce one trophy of each type)
recipe = {
    'football': {'wood': 4, 'plaque': 1, 'brass_football': 1, 'brass_soccer': 0},
    'soccer':   {'wood': 2, 'plaque': 1, 'brass_football': 0, 'brass_soccer': 1}
}

# Create a model instance
m = LpProblem("Maximize_Profit", LpMaximize)

# Define decision variables for the number of trophies
trophies = {sport: LpVariable(f"trophies_{sport}", lowBound=0, cat="Continuous") for sport in sports}

# Define the objective function: total profit
total_profit = lpSum([profit[sport] * trophies[sport] for sport in sports])

# Add the objective function to the model
m += total_profit

# Add the constraints: ensuring we do not exceed available ingredients
for ingredient in ingredients:
    m += lpSum([recipe[sport][ingredient] * trophies[sport] for sport in sports]) <= quant_avail[ingredient], f"Constraint_{ingredient}"

# Solve the problem
m.solve()

# Output results
print("Solution Status:", LpStatus[m.status])
for sport in sports:
    print(f"Number of {sport} trophies: {trophies[sport].varValue}")

print(f"Total profit is: ${value(total_profit)}")
