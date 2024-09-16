using JuMP,Clp

# this array stores the task names (:a, :b, ..., :x)
tasks = []
for i = 'a':'x'
    push!(tasks, Symbol(i))    # string(sym) converts back to a string, i.e. string(:hello) returns "hello"
end

# this dictionary stores the project durations
dur = [0, 4, 2, 4, 6, 1, 2, 3, 2, 4, 10, 3, 1, 2, 3, 2, 1, 1, 2, 3, 1, 2, 5, 0]
duration = Dict(zip(tasks,dur))

# this dictionary stores the projects that a given project depends on (ancestors)
pre = ( [], [:a], [:b], [:c], [:d], [:c], [:f], [:f], [:d], [:d,:g], [:i,:j,:h], [:k],
    [:l], [:l], [:l], [:e], [:p], [:c], [:o,:t], [:m,:n], [:t], [:q,:r], [:v], [:s,:u,:w])
pred = Dict(zip(tasks,pre))

using JuMP,Clp
m = Model(Clp.Optimizer)

@variable(m, tstart[tasks])

# one-line implementation of the constraints:
# @constraint(m, link[i in tasks, j in pred[i]], tstart[i] >= tstart[j] + duration[j])

for i in tasks
    for j in pred[i]
        @constraint(m, tstart[i] >= tstart[j] + duration[j])
    end
end
@constraint(m, tstart[:a] == 0)
@objective(m, Min, tstart[:x] + duration[:x])     # total duration is start time of last task + duration of last task.

optimize!(m)
println(value.(tstart))
println("minimum duration: ", objective_value(m))