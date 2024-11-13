import matplotlib.pyplot as plt
from keras.datasets import cifar10
(trainX, trainy), (testX, testy) = cifar10.load_data()

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# for i in range(10):
#     image = trainX[i]
#     label = trainy[i]
#
# plt.imshow(image)
# plt.axis('off')
# plt.title('CIFAR-10 Image: Class ' + str(label[0]) + ' (' + class_names[label[0]] + ')')
# plt.show()

# Set up the plot with a grid of 2 rows and 5 columns
plt.figure(figsize=(10, 5))

for i in range(10):
    image = trainX[i]
    label = trainy[i]

    # Set up a subplot (2 rows, 5 columns)
    plt.subplot(2, 5, i + 1)
    plt.imshow(image)
    plt.axis('off')  # Hide axis
    plt.title('Class ' + str(label[0]) + ' (' + class_names[label[0]] + ')')

# Show all images in the grid
plt.tight_layout()  # Adjust spacing between images for better display
plt.show()


# 2) The CIFAR-10 dataset is a supervised learning dataset used for classification tasks. It contains labeled data,
# with each image corresponding to a specific class from the 10 predefined categories
# (e.g., airplane, automobile, bird, etc.). It's commonly used for training and evaluating machine learning models,
# especially in the fields of computer vision and deep learning.
# 3) Inputs (Features): The inputs are the images in the dataset. Each image has 3 color channels (RGB) and is of
# size 32x32 pixels, making the input data for each image a 32x32x3 matrix.
# Outputs (Labels): The outputs are the class labels associated with each image. The CIFAR-10 dataset has 10
# possible classes, such as "airplane," "automobile," etc. The labels are represented as integers (0-9), where
# each integer corresponds to one of the 10 classes.
# 4) Diagram of the input-output-black box system
# Input: Images (32x32x3)
# Black Box: This is where a machine learning model (such as a convolutional neural network, CNN) learns the
# mapping from images to labels.
# Output: Predicted labels (0-9) corresponding to the class of each image.
# +-------------------+        +-------------------+
# |                   |        |                   |
# |     Input         | -----> |      Black Box    | -----> Output
# |   (Images)        |        |   (Machine        |        (Labels)
# |  (32x32x3)        |        |    Learning)      |
# |                   |        |                   |
# +-------------------+        +-------------------+
# 5) sShapes of the data
# Training data (trainX): The shape of the training data is (50000, 32, 32, 3), meaning there are 50,000 images,
# each of size 32x32 pixels, and with 3 color channels (RGB).
# Training labels (trainy): The shape of the training labels is (50000, 1), which corresponds to the class label
# for each image, with 50,000 labels.
# Test data (testX): The shape of the test data is (10000, 32, 32, 3), meaning there are 10,000 images for testing,
# each of the same size as the training data.
# Test labels (testy): The shape of the test labels is (10000, 1).

# Summary
# Type: Supervised learning, classification
# Inputs: Images (32x32x3)
# Outputs: Labels (10 classes)
# Shape: Training data is (50000, 32, 32, 3) and labels are (50000, 1);
# Test data is (10000, 32, 32, 3) and labels are (10000, 1).