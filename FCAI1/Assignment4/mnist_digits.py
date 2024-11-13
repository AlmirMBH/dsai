import matplotlib.pyplot as plt
from keras.datasets import mnist

# Load the MNIST dataset
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Print the shape of the data
print(f'Train images shape: {train_images.shape}')
print(f'Train labels shape: {train_labels.shape}')
print(f'Test images shape: {test_images.shape}')
print(f'Test labels shape: {test_labels.shape}')

# Visualize the first 10 images in the training set
plt.figure(figsize=(6, 3)) # Adjust figure size for smaller display

for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(train_images[i], cmap='gray', interpolation='nearest') # Use interpolation for smoother appearance
    plt.title(f'Label: {train_labels[i]}')
    plt.axis('off') # Turn off the axis

plt.tight_layout()
plt.show()
