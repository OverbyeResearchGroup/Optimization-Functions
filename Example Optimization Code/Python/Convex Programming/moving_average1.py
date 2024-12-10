import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

# Load data from csv you will need to change this path corresponding to your computer
raw = pd.read_csv('C:/Users/Owner/Downloads/uy_data.csv')

# Assuming the first column corresponds to 'u' and the second column to 'y'
u = raw.iloc[:, 0].values  # Convert to numpy array for easier manipulation
y = raw.iloc[:, 1].values
T = len(u)

# Plot the u and y data
plt.figure(figsize=(12, 4))
plt.plot(u, '.-', label='input u')
plt.plot(y, '.-', label='output y')
plt.legend(loc='lower right')
plt.show()
