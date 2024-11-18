import numpy as np
import matplotlib.pyplot as plt

# Load data (replace file paths as needed)
μ = 100 * np.genfromtxt("folio_mean.csv", delimiter=',')  # Expected return (in percent)
Σ = 10000 * np.genfromtxt("folio_cov.csv", delimiter=',')  # Expected variance (in percent squared)

# Calculate standard deviation from the diagonal of the covariance matrix
std_devs = np.sqrt(np.diag(Σ))

# Create scatter plot
plt.figure(figsize=(7, 5))
plt.plot(std_devs, μ, "b.")  # Blue dots for each asset
plt.xlabel("std deviation (%)")
plt.ylabel("expected return (%)")
plt.tight_layout()

# Save the figure (optional)
# plt.savefig("folio3_assets.pdf")

# Show the plot
plt.show()
