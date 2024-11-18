import numpy as np
import matplotlib.pyplot as plt

# Load covariance matrix (replace file path as needed)
Σ = 10000 * np.genfromtxt("folio_cov.csv", delimiter=',')  # Expected variance (in percent squared)

# Sort assets by expected return (use μ as in the previous code)
μ = 100 * np.genfromtxt("folio_mean.csv", delimiter=',')  # Expected return (in percent)
ix = np.argsort(μ)  # Indices for sorting

# Compute the correlation matrix
std_devs = np.sqrt(np.diag(Σ))
D_inv = np.diag(1 / std_devs)  # Diagonal matrix with 1/std deviations
corr = D_inv @ Σ @ D_inv  # Correlation matrix

# Create heatmap
plt.figure(figsize=(8, 8))
plt.imshow(corr[ix][:, ix], cmap="coolwarm", interpolation="nearest")  # Heatmap with sorted indices
plt.colorbar()  # Add a color bar
plt.axis("image")  # Set axis aspect ratio to "image" for square cells
plt.title("Correlation matrix for 225 assets")
plt.tight_layout()

# Save the figure (optional)
# plt.savefig("folio2_cov.pdf")

# Show the plot
plt.show()
