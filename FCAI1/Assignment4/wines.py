import pandas as pd
import matplotlib.pyplot as plt

# Adjust pandas display options for full output
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)     # Show all rows if needed

# The wines is a structured dataset
data = pd.read_csv("wines.csv")

# Extract features for plotting (first two features for X and Y)
x_feature = data['fixed acidity']
y_feature = data['volatile acidity']
labels = data['label']

# Create a figure and axis for the scatter plot
_, ax = plt.subplots()

# Plot a scatter plot of the first two features with specified color map and transparency
scatter = ax.scatter(x_feature, y_feature, c=labels, cmap='cool', alpha=0.2)

# Set the labels for the x and y axes
ax.set(xlabel='Fixed Acidity', ylabel='Volatile Acidity')

# Create a legend to show class color coding
legend = ax.legend(*scatter.legend_elements(), loc="lower right", title="Classes")
ax.add_artist(legend)

# Show the plot
plt.show()