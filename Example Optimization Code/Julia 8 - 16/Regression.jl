#Previous versions of this code used the Gurobi and/or Mosek optimizers, which require a licence. An academic license can be obtained from them if needed.  
using JuMP, HiGHS, ECOS, SCS, NonlinearSolve, PyPlot, Ipopt, LinearAlgebra, StaticArrays, Ipopt
# define (x,y) coordinates of the points
x = AbstractFloat[ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
y = AbstractFloat[ 1, 3, 0, 1, 2, 4, 6, 7, 5 ]

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

m = Model(Ipopt.Optimizer)
#m = Model(Gurobi.Optimizer)

@variable(m, u[i=1:k+1])
@objective(m, Min, sum( (y - A*u).^2 ) )

optimize!(m)
#println(m)
println(value.(u))

uopt

inv(A'*A)*(A'*y)

A\y

npts = 100
xfine = range(0,10,npts)
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

# NOTE: problem can be optimize!d using ECOS or SCS if written as an "SOCP" --- more on this later!
# Here is a working example:

#m = Model(optimizer_with_attributes(ECOS.Optmizer, "verbose" => false))
m = Model(Ipopt.Optimizer)
@variable(m, u[i=1:k+1])
@variable(m, t)
#expr = y .- (A * u)
#newexpr = normalize!(expr)
#It really, really does not want us to normalize this
#@constraint(m, y .- (A * u) <= t)
@constraint(m, normalize!(y - A*u) <= t)
@objective(m, Min, t)

optimize!(m)
uopt = value.(u)
println(m)
println(uopt)
