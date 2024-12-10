import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load data from csv you will need to change this path corresponding to your computer
raw = pd.read_csv('C:/Users/Owner/Downloads/uy_data.csv')

# Assuming the first column corresponds to 'u' and the second column to 'y'
u = raw.iloc[:, 0].values  # Convert to numpy array for easier manipulation
y = raw.iloc[:, 1].values
T = len(u)

# Initialize variables
MaxWidth = 40
errMA = np.zeros(MaxWidth)

# Compute moving average model error
for width in range(1, MaxWidth + 1):
    AMA = np.zeros((T, width))
    for i in range(width):
        AMA[i:, i] = u[:T-i]  # Adjusted for 0-based indexing
    wMA = np.linalg.lstsq(AMA, y, rcond=None)[0]  # Least squares solution
    yMAest = AMA @ wMA
    errMA[width - 1] = np.linalg.norm(y - yMAest)

# Plot the error as a function of window size
plt.figure(figsize=(8, 3))
plt.title("Error as a function of window size")
plt.plot(range(1, MaxWidth + 1), errMA, "b.-")
plt.xlabel("window size")
plt.ylabel("error")
plt.legend(["MA"], loc="right", fontsize=10)
plt.ylim([0, 6])
plt.show()
