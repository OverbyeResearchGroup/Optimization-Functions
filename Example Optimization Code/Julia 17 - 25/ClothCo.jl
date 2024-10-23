using JuMP, Cbc

m = Model(Cbc.Optimizer)

@variable(m, x[1:3] >= 0)
@variable(m, z[1:3], Bin)

@constraint(m, 3x[1] + 2x[2] + 6x[3] <= 150)  # labor budget
@constraint(m, 4x[1] + 3x[2] + 4x[3] <= 160)  # cloth budget
@constraint(m, x .<= 50*z)                    # if x>0 then z=1

@objective(m, Max, 6x[1] + 4x[2] + 7x[3] - 200z[1] - 150z[2] - 100z[3])

optimize!(m)

xopt = value.(x)
println(xopt[1], " shirts")
println(xopt[2], " shorts")
println(xopt[3], " pants" )
println()
println("\$", objective_value(m), " of net profit")