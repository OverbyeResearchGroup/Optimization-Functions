using JuMP, Clp, NamedArrays

# the types of trophies produced
sports = [:football, :soccer]

# ingredients involved
ingredients = [:wood, :plaque, :brass_football, :brass_soccer]

# profits returned (for each sport)
profit = Dict( zip( sports, [ 12, 9 ] ) )

# quantities available (for each ingredient)
quant_avail = Dict( zip( ingredients, [ 4800, 1750, 1000, 1500 ] ) )

# recipes (sport, ingredient)
recipe_mat = [ 4 1 1 0
               2 1 0 1 ]
recipe = NamedArray( recipe_mat, (sports,ingredients), ("sport","ingredient",) )

m = Model(Clp.Optimizer)

@variable(m, trophies[sports] >= 0 )
@expression(m, total_profit, sum( profit[s]*trophies[s] for s in sports) )
@constraint(m, constr[i in ingredients], sum( recipe[s,i]*trophies[s] for s in sports ) <= quant_avail[i] )
@objective(m, Max, total_profit )

optimize!(m)
println(value.(trophies))
println("Total profit is: \$", value(total_profit))




