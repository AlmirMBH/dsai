from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn import datasets

# Principal Component Analysis (PCA)
# Iris dataset 3D visualization - All features represented in three principal "features" called components
# Import the PCA class from sklearn’s decomposition module

# Load data
iris = datasets.load_iris()

# Create a figure for a 3D plot with specific size
fig = plt.figure(1, figsize=(8, 6))

# Create a 3D subplot with elevation and azimuth angle for better view
ax = fig.add_subplot(111, projection="3d", elev=-150, azim=110)

# Apply PCA to reduce the dataset to 3 components
X_reduced = PCA(n_components=3).fit_transform(iris.data)

# Create a 3D scatter plot using the first three principal components
ax.scatter(
    X_reduced[:, 0], # 1st principal component
    X_reduced[:, 1], # 2nd principal component
    X_reduced[:, 2], # 3rd principal component
    c=iris.target # Color points by the target class
)

# Set the labels for the plot axes
ax.set_xlabel("Income from Tarik and Haris over the next 6 months")
ax.set_ylabel("Hours overtime")
ax.set_zlabel("Late salary savings")

# Show the plot
plt.show()