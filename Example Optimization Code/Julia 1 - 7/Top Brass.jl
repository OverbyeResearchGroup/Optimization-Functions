using JuMP, Clp

m = Model(Clp.Optimizer)


@variable(m, 0 <= f <= 1000)           # football trophies
@variable(m, 0 <= s <= 1500)           # soccer trophies
@constraint(m, 4f + 2s <= 4800)        # total board feet of wood
@constraint(m, f + s <= 1750)          # total number of plaques
@objective(m, Max, 12f + 9s)           # maximize profit

status = optimize!(m)

println(status)
println("Build ", value(f), " football trophies.")
println("Build ", value(s), " soccer trophies.")
