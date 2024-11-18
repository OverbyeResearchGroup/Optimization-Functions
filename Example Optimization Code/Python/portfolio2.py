import numpy as np
import matplotlib.pyplot as plt

# Load data (replace file paths as needed)
μ = 100 * np.genfromtxt("folio_mean.csv", delimiter=',')  # Expected return (in percent)
Σ = 10000 * np.genfromtxt("folio_cov.csv", delimiter=',')  # Expected variance (in percent squared)

# Sort assets by expected return
ix = np.argsort(μ)  # Indices for sorting

# Create plots
fig = plt.figure(figsize=(12, 6))

# Subplot 1: Standard deviation
plt.subplot(211)
plt.xlim(0, 225)
plt.plot(np.sqrt(np.diag(Σ))[ix], "g")
plt.ylabel("Standard deviation (%)")
plt.title("Standard deviation and expected return of all 225 assets")
plt.tight_layout()

# Subplot 2: Expected return
plt.subplot(212)
plt.xlim(0, 225)
plt.plot(μ[ix])
plt.plot([0, 225], [0, 0], "r--")  # Horizontal line at y=0
plt.ylabel("Expected return (%)")
plt.tight_layout()

# Save the figure (optional)
# plt.savefig("folio1_vals.pdf")

# Show the plots
plt.show()
