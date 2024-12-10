import numpy as np
import matplotlib.pyplot as plt

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

# Plotting the contour plot
plt.figure(figsize=(6, 5))
plt.contour(xv, yv, res, 60, origin="lower", extent=(0, 3.5, 0, 3.5))
plt.plot(locs[:, 0], locs[:, 1], "bo", label="Beacons")
plt.plot(truepos[0], truepos[1], "ro", label="True position")
plt.xlabel("u")
plt.ylabel("v")
plt.colorbar()
plt.tight_layout()

# Show plot
plt.show()
