#include "DataManager.h"
#include <fstream>
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#include <cmath>

const int MNIST_IMAGE_HEADER_SIZE = 16;
const int MNIST_LABEL_HEADER_SIZE = 8;
const int NUMPY_HEADER_SIZE = 80;
const int IMAGE_PIXELS = 784;
const int TRAINING_SAMPLES_LIMIT = 5000;

/**
 * Open binary files containing handwritten digits and labels. 
 * Skip the file headers and stores the pixel values into the dataset.
 */
bool DataManager::loadMNIST(std::string imagePath, std::string labelPath, Dataset& dataset) {
    std::ifstream imageFile(imagePath, std::ios::binary);
    std::ifstream labelFile(labelPath, std::ios::binary);
    if (!imageFile || !labelFile) {
        return false;
    }
    
    // Skip the file headers defined by the MNIST dataset creators (16 bytes for images, 8 for labels).
    imageFile.seekg(MNIST_IMAGE_HEADER_SIZE); 
    labelFile.seekg(MNIST_LABEL_HEADER_SIZE);

    for (int sampleIndex = 0; sampleIndex < TRAINING_SAMPLES_LIMIT; ++sampleIndex) {
        std::vector<double> featureValues;
        for (int pixelIndex = 0; pixelIndex < IMAGE_PIXELS; ++pixelIndex) {
            unsigned char pixelValue = 0;
            imageFile.read((char*)&pixelValue, 1);
            featureValues.push_back(pixelValue / 255.0);
        }
        unsigned char labelValue = 0;
        labelFile.read((char*)&labelValue, 1);
        dataset.add(FeatureVector(featureValues), labelValue);
    }
    return true;
}

/**
 * Load a single image file from the disk. Convert the 
 * image into a format the system can process (28x28 pixels).
 */
bool DataManager::loadImage(std::string path, Image& image) {
    int origWidth, origHeight, channelCount;
    unsigned char* imageData = stbi_load(path.c_str(), &origWidth, &origHeight, &channelCount, 1);
    if (!imageData) {
        return false;
    }
    
    // Resize the image to 28x28 so the models can process it correctly.
    // We use a simple method that picks the nearest pixel from the original image.
    std::vector<uint8_t> resizedData;
    resizedData.reserve(784);
    for (int y = 0; y < 28; ++y) {
        for (int x = 0; x < 28; ++x) {
            int srcX = (x * origWidth) / 28;
            int srcY = (y * origHeight) / 28;
            resizedData.push_back(imageData[srcY * origWidth + srcX]);
        }
    }
    
    image = Image(28, 28, resizedData);
    
    // If the image is mostly light (black-on-white), we invert it to match MNIST (white-on-black).
    int totalBrightness = 0;
    for (uint8_t pixel : resizedData) {
        totalBrightness += pixel;
    }
    if (totalBrightness / 784 > 128) {
        for (int y = 0; y < 28; ++y) {
            for (int x = 0; x < 28; ++x) {
                image.setPixel(x, y, 255 - image.getPixel(x, y));
            }
        }
    }

    stbi_image_free(imageData);
    return true;
}

/**
 * Load patterns from a specialized binary file. Skip 
 * the file header and store a limited number of samples into the dataset.
 */
bool DataManager::loadNumpy(std::string path, Dataset& dataset, int label, int maxSamples) {
    std::ifstream binaryFile(path, std::ios::binary);
    if (!binaryFile) {
        return false;
    }

    // Skip the 80-byte header used in the Numpy (.npy) file format.
    binaryFile.seekg(NUMPY_HEADER_SIZE);
    for (int sampleIndex = 0; sampleIndex < maxSamples; ++sampleIndex) {
        std::vector<double> featureValues;
        for (int pixelIndex = 0; pixelIndex < IMAGE_PIXELS; ++pixelIndex) {
            unsigned char pixelValue = 0;
            if (!binaryFile.read((char*)&pixelValue, 1)) {
                break;
            }
            featureValues.push_back(pixelValue / 255.0);
        }
        if (featureValues.size() < IMAGE_PIXELS) {
            break;
        }
        dataset.add(FeatureVector(featureValues), label);
    }
    return true;
}

/**
 * Load circle, square, and triangle patterns from the datasets folder.
 */
void DataManager::loadShapes(Dataset& dataset, int samplesPerClass) {
    loadNumpy("../datasets/circle.npy", dataset, 0, samplesPerClass);
    loadNumpy("../datasets/square.npy", dataset, 1, samplesPerClass);
    loadNumpy("../datasets/triangle.npy", dataset, 2, samplesPerClass);
}

/**
 * Load star, zigzag, and lightning patterns from the datasets folder.
 */
void DataManager::loadSymbols(Dataset& dataset, int samplesPerClass) {
    loadNumpy("../datasets/full_numpy_bitmap_star.npy", dataset, 0, samplesPerClass);
    loadNumpy("../datasets/full_numpy_bitmap_zigzag.npy", dataset, 1, samplesPerClass);
    loadNumpy("../datasets/full_numpy_bitmap_lightning.npy", dataset, 2, samplesPerClass);
}
