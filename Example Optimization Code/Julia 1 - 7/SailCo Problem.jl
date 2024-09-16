using JuMP, Clp

d = [40 60 70 25]                   # monthly demand for boats

m = Model(Clp.Optimizer)

@variable(m, 0 <= x[1:4] <= 40)       # boats produced with regular labor
@variable(m, y[1:4] >= 0)             # boats produced with overtime labor
@variable(m, h[1:5] >= 0)             # boats held in inventory
@constraint(m, h[1] == 10)
@constraint(m, flow[i in 1:4], h[i]+x[i]+y[i]==d[i]+h[i+1])     # conservation of boats
@objective(m, Min, 400*sum(x) + 450*sum(y) + 20*sum(h))         # minimize costs

optimize!(m)

println("Build ", Array{Int}(value.(x')), " using regular labor")
println("Build ", Array{Int}(value.(y')), " using overtime labor")
println("Inventory: ", Array{Int}(value.(h')))

