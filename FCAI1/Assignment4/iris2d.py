from sklearn import datasets
import matplotlib.pyplot as plt

# IRIS DATASET 2D VISUALIZATION

# Load the data
iris = datasets.load_iris()

# Create a figure and axis for the scatter plot
_, ax = plt.subplots()

# Plot a scatter plot of the first two features of the iris dataset
scatter = ax.scatter(iris.data[:, 0], iris.data[:, 1], c=iris.target)

# Set the labels for the x and y axes using the feature names from the iris dataset
ax.set(xlabel='sepal length (cm)', ylabel='sepal width (cm)')

# Create a legend for the scatter plot, showing which color corresponds to each class (species)
# This line only passes the list of handles (scatter.legend_elements()[0]) to the legend, while manually
# setting iris.target_names as labels. This works if you explicitly know the labels and want to specify them
legend = ax.legend(scatter.legend_elements()[0], iris.target_names, loc="lower right", title="Classes")

# The '*' unpacks the returned tuple, so that we do not have to
# The first part (handles) and the second part (labels) are passed automatically to ax.legend.
# This line uses both the handles and labels generated directly from scatter.legend_elements() without needing
# to specify iris.target_names separately as in the previous example
# legend = ax.legend(*scatter.legend_elements(), loc="lower right", title="Classes")

ax.add_artist(legend)  # Add the legend to the plot

# Show the plot
plt.show()