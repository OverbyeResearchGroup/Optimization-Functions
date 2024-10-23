
using Random, JuMP, Cbc, Ipopt, GLPK, LinearAlgebra, Statistics

nI = 50  # number of facilities
nJ = 50  # number of customers

# generate random problem instance
Random.seed!(1)
f = rand(nI)
#f = 0.5*ones(nI)
c = rand(nI,nJ)

#using JuMP, Cbc Gurobi, Mosek, GLPKMathProgInterface, Cbc
#m = Model(solver = GLPKSolverMIP())
#m = Model(solver = CbcSolver())
m = Model(Cbc.Optimizer)
#m = Model(Ipopt.Optimizer)
#m = Model(solver = MosekSolver())
#m = Model(solver = GurobiSolver(OutputFlag=false))

@variable(m, x[1:nI], Bin)         # binary constraint
#@variable(m, 1 >= x[1:nI] >= 0)    # LP relaxation

@variable(m, y[1:nI,1:nJ], Bin)     # binary constraint
#@variable(m, y[1:nI,1:nJ] >= 0)   # LP relaxation

@constraint(m, cc[j = 1:nJ], sum( y[i,j] for i=1:nI ) == 1)

# choose one of these two constraints (they are equivalent)
#@constraint(m, cr[i=1:nI], sum( y[i,j] for j=1:nJ ) <= nJ*x[i])
@constraint(m, cr[i=1:nI,j=1:nJ], y[i,j] <= x[i])

@objective(m, Min, dot(f,x) + dot(c,y))

@time(optimize!(m))

#using JuMP, Cbc, Gurobi, Mosek, GLPKMathProgInterface, Cbc

nvals = [5,10,15,20,25,30,35,40,45,50]
tt_glpk = zeros(length(nvals),50)
tt_cbc = zeros(length(nvals),50)
tt_mosek = zeros(length(nvals),50)
tt_gurobi = zeros(length(nvals),50)

t = tt_glpk
for count = 1:50
    println(count)
    for (k,n) in enumerate(nvals)
        nI = n  # number of facilities
        nJ = n  # number of customers

        # generate random problem instance
        Random.seed!(count)
        f = 0.5*ones(nI)
        c = rand(nI,nJ)

        m = Model(GLPK.Optimizer)
        #m = Model(solver = GLPKSolverMIP())
        #m = Model(solver = CbcSolver())
        #m = Model(solver = MosekSolver())
        #m = Model(solver = GurobiSolver(OutputFlag=false))

        @variable(m, x[1:nI], Bin)         # binary constraint
        @variable(m, y[1:nI,1:nJ] >= 0)    # LP relaxation
        @constraint(m, cc[j = 1:nJ], sum( y[i,j] for i=1:nI ) == 1)
        @constraint(m, cr[i=1:nI,j=1:nJ], y[i,j] <= x[i])
        @objective(m, Min, dot(f,x) + dot(c,y))
        t[k,count] = @timed(optimize!(m))[2]
    end
end

tt_gurobi_mean = mean(tt_gurobi,dims=2)
tt_mosek_mean = mean(tt_mosek,dims=2)
tt_cbc_mean = mean(tt_cbc,dims=2)
tt_glpk_mean = mean(tt_glpk,dims=2)

using PyPlot

figure(figsize=(10,4))
semilogy(nvals,tt_glpk_mean,label="GLPK")
semilogy(nvals,tt_cbc_mean,label="Cbc")
semilogy(nvals,tt_mosek_mean,label="Mosek")
semilogy(nvals,tt_gurobi_mean,label="Gurobi")
legend(loc="best")
xlabel("number of facilities and customers")
ylabel("time to solve (seconds)")
title("comparison of different solvers")
tight_layout()
PyPlot.show()
savefig("solver_comparison.pdf")