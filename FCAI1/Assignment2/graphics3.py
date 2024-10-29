import numpy as np
import matplotlib.pyplot as plt

# Generate 100 random points for x and y
x = np.random.randn(100)
y = np.random.randn(100)

# Create a scatter plot
plt.figure(figsize=(10, 6))

# Plot points with different colors based on the condition
plt.scatter(x[x > 0], y[x > 0], color='blue', label='x > 0')
plt.scatter(x[x <= 0], y[x <= 0], color='red', label='x ≤ 0')

# Add labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Scatter Plot of Random Points with Normal Distribution')
plt.legend()

plt.grid()
plt.show()
