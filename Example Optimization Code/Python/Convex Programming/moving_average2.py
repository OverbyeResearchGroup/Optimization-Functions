import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

# Load data from csv you will need to change this path corresponding to your computer
raw = pd.read_csv('C:/Users/Owner/Downloads/uy_data.csv')

# Assuming the first column corresponds to 'u' and the second column to 'y'
u = raw.iloc[:, 0].values  # Convert to numpy array for easier manipulation
y = raw.iloc[:, 1].values
T = len(u)
# Assuming u and y have been defined already, and T is the length of u
width = 3
A = np.zeros((T, width))

for i in range(width):
    A[i:, i] = u[:T-i]  # Adjusted to 0-based indexing in Python

# Solve for wopt using least squares
wopt = np.linalg.lstsq(A, y, rcond=None)[0]

# Compute the estimated output
yest = A @ wopt

# Plot the true output and predicted output
plt.figure(figsize=(12, 4))
plt.plot(y, "g.-", label="true output")
plt.plot(yest, "m.-", label="predicted output")
plt.legend(loc="lower right")
plt.title("Moving average model")
plt.show()

# Print the norm of the difference between y and yest
print(np.linalg.norm(yest - y))
