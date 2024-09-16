import JuMP, Clp
using JuMP, Clp, LinearAlgebra

A = AbstractFloat[2 -1 2; -1 2 4; 1 2 -2; -1 0 0; 0 -1 0; 0 0 -1];
b = AbstractFloat[2; 16; 8; 0; 0; 0]

using JuMP, Clp, LinearAlgebra



m = Model(Clp.Optimizer)
@variable(m, r >= 0)           # radius
@variable(m, x[1:3])           # coordinates of center
for i = 1:size(A,1)
    @constraint(m, A[i,:]'.*x .+ r.*normalize!(A[i,:]) .<= b[i])
end
@objective(m, Max, r)     # maximize radius

optimize!(m)
center = value.(x)
radius = value.(r)
status = objective_value(m)
println(status)
println("The coordinates of the Chebyshev center are: ", center)
println("The largest possible radius is: ", radius)

