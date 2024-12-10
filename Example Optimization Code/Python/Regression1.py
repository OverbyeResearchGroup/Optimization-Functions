import matplotlib.pyplot as plt

# Define (x, y) coordinates of the points
x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
y = [1, 3, 0, 1, 2, 4, 6, 7, 5]

# Create a figure
plt.figure(figsize=(8, 4))

# Plot the points
plt.plot(x, y, "r.", markersize=10)

# Set axis limits
plt.axis([0, 10, -2, 8])

# Enable grid
plt.grid(True)

# Show the plot
plt.show()
