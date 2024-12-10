from pulp import LpStatus, LpMaximize, LpProblem, LpVariable, value

#define the problem
model = LpProblem("Maximize Profit", LpMaximize)

#define variables
f = LpVariable('f', lowBound= 0)
s = LpVariable('s', lowBound = 0)

#define constraints
model += 4*f + 2*s <= 4800 #Cwood
model += f + s <= 1750   #Cplaques
model += f <= 1000  #Cfballs
model += s <= 1500  #Csballs

#define objectives
model += 12*f + 9*s #maximize profit

status = model.solve()

print(f"Status: {LpStatus[status]}")
if status == 1:
    print(f"Build {value(f)} football trophies.")
    print(f"Build {value(s)} soccer trophies.")
    print(f"Total profit will be ${value(model.objective)}")
else:
    print("No optimal solution found.")

