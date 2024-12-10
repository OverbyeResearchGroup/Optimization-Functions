import numpy as np
import matplotlib.pyplot as plt

# Seed the random number generator for reproducibility
np.random.seed(1)

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

# Generate measurements (distances to true position)
ymeas = np.sqrt(np.sum((locs - truepos)**2, axis=1))

# Optional: Add noise (uncomment to add noise)
# noise = 0.4 * (np.random.randn(n) - 0.5)
# ymeas += noise

# Plotting
plt.figure(figsize=(5, 5))
plt.plot(truepos[0], truepos[1], "ro", label="True position")
plt.plot(locs[:, 0], locs[:, 1], "bo", label="Beacons")
plt.legend(numpoints=1, loc="upper center", bbox_to_anchor=(0.5, 1.05))
plt.axis([0, 3.5, 0, 3.5])
plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()

# Show plot
plt.show()
