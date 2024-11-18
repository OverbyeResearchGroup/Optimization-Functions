import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(0)

# Generate random data
X = 2 + 5 * np.random.randn(100, 16)

# Plot 1: Single sample vs averaged samples
plt.figure(figsize=(12, 3))
plt.plot(range(1, 101), X[:, 0], label="single sample")
plt.plot(range(1, 101), np.mean(X, axis=1), label="avg of 16 samples")
plt.plot(range(1, 101), 2 * np.ones(100), "r--", label="mean value")
plt.legend(loc="lower right")
plt.title("Comparison of a single sample vs 16 averaged samples")
plt.grid()
plt.show()

# Plot 2: Sorted single sample vs sorted averaged samples
plt.figure(figsize=(12, 3))
plt.plot(range(1, 101), np.sort(X[:, 0]), label="single sample")
plt.plot(range(1, 101), np.sort(np.mean(X, axis=1)), label="avg of 16 samples")
plt.plot(range(1, 101), 2 * np.ones(100), "r--", label="mean value")
plt.legend(loc="lower right")
plt.title("Sorted single sample vs sorted averaged sample")
plt.grid()
plt.show()
