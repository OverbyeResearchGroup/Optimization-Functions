

# define (x,y) coordinates of the points
x = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
y = [ 1, 3, 0, 1, 2, 4, 6, 7, 5 ]

using PyPlot
figure(figsize=(8,4))
plot(x,y,"r.", markersize=10)
axis([0,10,-2,8])
grid("on")
# order of polynomial to use
k = 3

# fit using a function of the form f(x) = u1 x^k + u2 x^(k-1) + ... + uk x + u{k+1}
n = length(x)
A = zeros(n,k+1)
for i = 1:n
    for j = 1:k+1
        A[i,j] = x[i]^(k+1-j)
    end
end

# NOTE: must have either Gurobi or Mosek installed!

using JuMP, Gurobi, LinearAlgebra

#m = Model(solver=MosekSolver(LOG=0))
m = Model(Gurobi.Optimizer)
#m = Model(solver=GurobiSolver(OutputFlag=1,NumericFocus=2))    # extra option to do extra numerical conditioning
#m = Model(solver=GurobiSolver(OutputFlag=1,BarHomogeneous=1))  # extra option to use alternative algorithms

@variable(m, u[1:k+1])
@objective(m, Min, sum( (y - A*u).^2 ) )

status = optimize!(m)
uopt = value.(u)
println(status)

inv(A'*A)*(A'*y)

A\y

using PyPlot
npts = 100
xfine = LinRange(0,10,npts)
ffine = ones(npts)
for j = 1:k
    global ffine = [ffine.*xfine ones(npts)]
end
yfine = ffine * uopt
figure(figsize=(8,4))
plot( x, y, "r.", markersize=10)
plot( xfine, yfine, "b-")
axis([0,10,-2,8])
grid()
# NOTE: problem can be solved using ECOS or SCS if written as an "SOCP" --- more on this later!
# Here is a working example:
#EK NOTE: Neither ECOS or SCS handle his norm function in this code. 
# using JuMP, ECOS, SCS

# m = Model(ECOS.Optimizer)
# #m = Model(SCS.Optimizer)

# @variable(m, u[1:k+1])
# @variable(m, t)
# @constraint(m, norm(y - A*u) <= t)
# @objective(m, Min, t)

# status = solve(m)
# uopt = getvalue(u)
# println(status)
# println(uopt)



