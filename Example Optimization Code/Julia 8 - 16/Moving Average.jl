import Pkg; Pkg.add("CSV")
import Pkg; Pkg.add("DataFrames")
import Pkg; Pkg.add("PyPlot")
using CSV, DataFrames, LinearAlgebra
# Load the data file (ref: Boyd/263)
raw = DataFrame(CSV.File("./uy_data.csv"))
u = raw[:,1];
y = raw[:,2];
T = length(u)

# plot the u and y data
using PyPlot
figure(figsize=(12,4))
plot([u y],".-");
legend(["input u", "output y"], loc="lower right");

# generate A matrix. Using more width creates better fit.  (MA model)
width = 3
A = zeros(T,width)
for i = 1:width
    A[i:end,i] = u[1:end-i+1]
end
wopt = A\y
yest = A*wopt

figure(figsize=(12,4))
plot(y,"g.-",yest,"m.-")
legend(["true output", "predicted output"], loc="lower right");
title("Moving average model");
println()
println(normalize!(yest-y))

# compute the error that the moving average model makes
MaxWidth = 40
errMA = zeros(MaxWidth)
for width = 1:MaxWidth
    AMA = zeros(T,width)
    for i = 1:width
        AMA[i:end,i] = u[1:end-i+1]
    end
    wMA = AMA\y
    yMAest = AMA*wMA
    errMA[width] = norm(y-yMAest)
end
figure(figsize=(8,3))
title("Error as a function of window size")
plot(1:MaxWidth,errMA,"b.-")
xlabel("window size")
ylabel("error")
legend(["MA"],loc="right",fontsize=10)
ylim([0,6])
PyPlot.display_figs()
;