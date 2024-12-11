using Random, Statistics

# randomly generate a sorted list of numbers
Random.seed!(0)
N = 9
y = sort(10*rand(N))

# minimize the 2-norm
using JuMP, Gurobi
m = Model(Gurobi.Optimizer)
@variable(m, x)
@objective(m, Min, sum( (y.-x).^2 ) )

optimize!(m)

println("The optimal x value is: ", value(x))
mean(y)
# minimize the 1-norm
using JuMP
m = Model(Gurobi.Optimizer)
@variable(m, x)
@variable(m, t[1:N])
@constraint(m, y.-x .<= t )
@constraint(m, -t .<= y.-x )
@objective(m, Min, sum(t) )

optimize!(m)

println("The optimal x value is: ", value(x))

median(y)

y[5]

# minimize the infinity-norm
using JuMP
m = Model(Gurobi.Optimizer)
@variable(m, x)
@variable(m, r)
@constraint(m, y.-x .<= r )
@constraint(m, -r .<= y.-x )
@objective(m, Min, r )

optimize!(m)

println("The optimal x value is: ", value(x))
(y[1] + y[N])/2

#Gets a different result than the example. Not sure what to do about that - EK