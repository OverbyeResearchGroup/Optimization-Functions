# this solution uses NamedArrays, which are arrays indexed over sets for both x and y dimensions.

using JuMP, Clp, NamedArrays

sites = [ 1,  2,  3]
mills = [:A, :B, :C]

cost_per_haul = 4    # don't forget the return trip!

dist = NamedArray( [8 15 50; 10 17 20; 30 26 15], (sites,mills), ("Sites","Mills") )
supply = Dict(zip( sites, [20 30 45] ))
demand = Dict(zip( mills, [30 35 30] ))

m = Model(Clp.Optimizer)

@variable(m, x[sites,mills] >= 0)          # x[i,j] is lumber shipped from site i to mill j.

@constraint(m, sup[i in sites], sum(x[i,j] for j in mills) == supply[i] )   # supply constraint
@constraint(m, dem[j in mills], sum(x[i,j] for i in sites) == demand[j] )   # demand constraint

@objective(m, Min, cost_per_haul*sum(x[i,j]*dist[i,j] for i in sites, j in mills))      # minimize transportation cost

optimize!(m)

# nicely formatted solution
solution = NamedArray( Int[value.(x[i,j]) for i in sites, j in mills], (sites,mills), ("Sites","Mills") )
println(solution)
println()
println("Total cost will be \$", objective_value(m))