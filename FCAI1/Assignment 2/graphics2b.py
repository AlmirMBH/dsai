import numpy as np
import matplotlib.pyplot as plt

"""
Repeat the previous task, but now plot the signals x and y in the same window (but on different subplots).
Add appropriate labels and titles for both plots.
"""

n = np.arange(1, 101)
x = np.sin(n)
y = np.cos(n)

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# Plot x = sin(n) in the first subplot
ax1.plot(n, x, color='blue')
ax1.set_title('Plot of x = sin(n)')
ax1.set_xlabel('n')
ax1.set_ylabel('sin(n)')
ax1.grid()

# Plot y = cos(n) in the second subplot
ax2.plot(n, y, color='red')
ax2.set_title('Plot of y = cos(n)')
ax2.set_xlabel('n')
ax2.set_ylabel('cos(n)')
ax2.grid()

plt.tight_layout()
plt.show()
