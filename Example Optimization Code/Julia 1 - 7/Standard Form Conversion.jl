using JuMP, Clp

m = Model(Clp.Optimizer)
@variable(m, p )
@variable(m, 1 <= q <= 4 )
@constraint(m, 5p - 3q == 7 )
@constraint(m, 2p + q >= 2 )
@objective(m, Min, p + q )

optimize!(m)

println(m)
println()
println("p = ", value(p) )
println("q = ", value(q) )
println("objective = ", objective_value(m) )
