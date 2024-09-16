using JuMP, Clp

m = Model(Clp.Optimizer)
@variable(m, f >= 0)                        # football trophies
@variable(m, s >= 0)                        # soccer trophies
@constraint(m, Cwood,   4f + 2s <= 4800)    # total board feet of wood
@constraint(m, Cplaques,  f + s <= 1750)    # total number of plaques
@constraint(m, Cfballs,       f <= 1000)    # total number of brass footballs
@constraint(m, Csballs,       s <= 1500)    # total number of brass soccer balls
@objective(m, Max, 12f + 9s)                # maximize profit

optimize!(m)

display(m)

println("Build ", value(f), " football trophies.")
println("Build ", value(s), " soccer trophies.")
println("Total profit will be \$", objective_value(m))
println("Dual variable for wood: ", dual(Cwood))
println("Dual variable for plaques: ", dual(Cplaques))
println("Dual variable for brass footballs: ", dual(Cfballs))
println("Dual variable for brass soccer balls: ", dual(Csballs))

m = Model(Clp.Optimizer)
@variable(m, λ[1:4] >= 0)
@constraint(m, 4λ[1] + λ[2] + λ[3] >= 12)
@constraint(m, 2λ[1] + λ[2] + λ[4] >= 9)
@objective(m, Min, 4800λ[1] + 1750λ[2] + 1000λ[3] + 1500λ[4])

optimize!(m)

display(m)

println("dual variables are: ", value.(λ))
println("Optimal objective is: ", objective_value(m))