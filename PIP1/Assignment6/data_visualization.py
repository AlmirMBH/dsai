import numpy as np
import matplotlib.pyplot as mp

#creating the data for the plot
x = np.linspace(0.0, 1.0, 1000)
y = np.sin(20*x)

#creating the window for the plot
mp.figure()

#creating the plot with the created data
mp.plot(x, y)

#enabling grid
mp.grid(True)

#displaying the plot
mp.show()