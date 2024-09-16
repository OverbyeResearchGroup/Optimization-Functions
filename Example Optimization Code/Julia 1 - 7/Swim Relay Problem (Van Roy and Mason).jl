using JuMP, Clp, NamedArrays

strokes = [ :backstroke, :breaststroke, :butterfly, :freestyle ]
names = [ :Carl, :Chris, :David, :Tony, :Ken ]

raw = [ 37.7 32.9 33.8 37.0 35.4
        43.4 33.1 42.2 34.7 41.8
        33.3 28.5 38.9 30.4 33.6
        29.2 26.4 29.6 28.5 31.1 ]

times = NamedArray( raw, (strokes,names), ("stroke","name"))

m = Model(Clp.Optimizer)

@variable(m, x[strokes,names] >= 0)

# each swimmer swims at most one event
@constraint(m, a[j in names], sum(x[i,j] for i in strokes) <= 1)

# each event has exactly one swimmer
@constraint(m, b[i in strokes], sum(x[i,j] for j in names) == 1)

@objective(m, Min, sum( x[i,j]*times[i,j] for i in strokes, j in names))

optimize!(m)

assignment = NamedArray([(value.(x[i,j])) for i in strokes, j in names ], (strokes, names), ("stroke","name"))