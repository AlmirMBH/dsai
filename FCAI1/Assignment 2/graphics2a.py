import numpy as np
import matplotlib.pyplot as plt

"""
Given the function x=sin(n) with 100 points (where n=1:100), plot the line graph of this function. Add
appropriate labels and a title. Then, overlay the graph with the function y=cos(n), also with 100 samples.
Include a grid on the plot.
"""

n = np.arange(1, 101)
x = np.sin(n)
y = np.cos(n)

plt.figure(figsize=(10, 6))
plt.plot(n, x, label='x = sin(n)', color='blue', linestyle='-')
plt.plot(n, y, label='y = cos(n)', color='red', linestyle='--')

# Add labels and title
plt.xlabel('n')
plt.ylabel('Function Values')
plt.title('Plot of x = sin(n) and y = cos(n)')

plt.legend()
plt.grid()
plt.show()
