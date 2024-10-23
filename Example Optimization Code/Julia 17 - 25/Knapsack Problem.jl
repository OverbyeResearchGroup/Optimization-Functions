using JuMP, Cbc
m = Model(Cbc.Optimizer)
@variable(m, z[1:5], Bin )
@constraint(m, 12z[1] + 2z[2] + 4z[3] + z[4] + z[5] <= 15)
@objective(m, Max, 4z[1] + 2z[2] + 10z[3] + 2z[4] + 1z[5])

optimize!(m)

println(m)
println()
println("z = ", value.(z) )
println("objective = ", objective_value(m) )

# parameters for our problem
w = [12, 2, 4, 1, 1]  # weights
v = [4, 2, 10, 2, 1]  # values
W = 15                # weight limit
n = length(w);        # number of items

m = Model(Cbc.Optimizer)
@variable(m, z[1:n], Bin )
@constraint(m, sum( w[i]*z[i] for i=1:n) <= W )
@objective(m, Max, sum( v[i]*z[i] for i=1:n) )

optimize!(m)

println(m)
println()
println("z = ", value.(z) )
println("objective = ", objective_value(m) )
