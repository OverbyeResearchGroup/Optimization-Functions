function news2i(a,i...)
    s2i = LinearIndices(a)
    s2i[i...]
end
println("Start \n")

using JuMP, Ipopt, LinearAlgebra

### MAKING A BRIDGE

Nx = 15
Ny = 7
N = (15, 7)

# FIXED NODES
fixed = [ news2i(N,1,1), news2i(N,Nx,1)]

# uniform load
loaded = [ (news2i(N,j,1), 0,1) for j = 1:Nx ]

# point load
loaded = [ (news2i(N,Int((Nx+1)/2),1), 0,Nx) ]

N2 = Nx*Ny  # number of nodes

# NODES: columns are x and y components respectively
nodes = [ kron(ones(Ny),collect(1:Nx)) kron(collect(1:Ny),ones(Nx)) ]

M = Int(N2*(N2-1)/2)  # number of edges

# EDGES: columns are the indices of the nodes at either end
edges = Array{Int}(zeros(M,2))

k = 0
for i = 1:N2
    for j = 1:i-1
        global k = k+1
        edges[k,:] = [i j]
    end
end

ℓ = zeros(M)
nx = zeros(N2,M)
ny = zeros(N2,M)
for j = 1:M
    i1 = edges[j,1]
    i2 = edges[j,2]
    ℓ[j] = norm( [nodes[i1,1]-nodes[i2,1], nodes[i1,2]-nodes[i2,2]] )
    nx[i1,j] = (nodes[i1,1]-nodes[i2,1])/ℓ[j]
    nx[i2,j] = (nodes[i2,1]-nodes[i1,1])/ℓ[j]
    ny[i1,j] = (nodes[i1,2]-nodes[i2,2])/ℓ[j]
    ny[i2,j] = (nodes[i2,2]-nodes[i1,2])/ℓ[j]
end

fx = zeros(N2)
fy = zeros(N2)
for L in loaded
    ind = L[1]
    fx[ind] = L[2]
    fy[ind] = L[3]
end

m = Model(Ipopt.Optimizer)

@variable(m, x[1:M] >= 0)   # area of edge from i to j
@variable(m, u[1:M] )       # force in edge from i to j

for i = 1:N2
    if i in fixed
        continue
    else
        @constraint(m, sum(u[j]*nx[i,j] for j=1:M) + fx[i] == 0 )
        @constraint(m, sum(u[j]*ny[i,j] for j=1:M) + fy[i] == 0 )
    end
end

@constraint(m, -x .<= u)
@constraint(m,  u .<= x)

@objective(m, Min, sum(ℓ[j]*x[j] for j=1:M))

optimize!(m)
xopt = value.(x);
uopt = value.(u)

using PyPlot

PyPlot.figure(figsize=((Nx+1)/2,(Ny+1)/2))

PyPlot.plot( nodes[:,1], nodes[:,2], "b." )
for j = 1:M
    if xopt[j] > 0
        i1 = edges[j,1]
        i2 = edges[j,2]
        PyPlot.plot( nodes[[i1,i2],1], nodes[[i1,i2],2], "r-", linewidth=sqrt(xopt[j]) )
    end
end
axis("equal")
axis([0,Nx+1,0,Ny+1])
PyPlot.display_figs()