import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Beacon locations
locs = np.array([[1.5, 1.5],
                 [1.5, 2.0],
                 [1.9, 2.5],
                 [2.0, 1.7],
                 [2.5, 1.5]])

# True position
truepos = np.array([1.0, 1.0])

# Number of beacons
n = locs.shape[0]

# Measurement distances (distances from the true position)
ymeas = np.sqrt(np.sum((locs - truepos)**2, axis=1))

# Create a grid of u and v values
xv = np.linspace(0, 3.5, 351)
yv = np.linspace(0, 3.5, 351)

# Initialize the result array
res = np.zeros((len(yv), len(xv)))

# Calculate the cost function (sum of squared differences)
for i, y in enumerate(yv):
    for j, x in enumerate(xv):
        distances = np.sqrt(np.sum((locs - np.array([x, y]))**2, axis=1))
        res[i, j] = np.sum((distances - ymeas)**2)

# Create a meshgrid for X and Y
X, Y = np.meshgrid(xv, yv)

# Plotting the 3D surface and contour plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# 3D surface plot
surf = ax.plot_surface(X, Y, res + 5, rstride=8, cstride=8, cmap="rainbow", edgecolor="black", linewidth=0.5)

# Contour plot on the surface
contour = ax.contour(X, Y, res, 60, zdir="z", offset=0, linewidths=0.5)

# Labels
ax.set_xlabel("u")
ax.set_ylabel("v")
ax.set_zlabel("Cost Function Value")

# Colorbar for surface plot
fig.colorbar(surf)

plt.tight_layout()

# Show plot
plt.show()
