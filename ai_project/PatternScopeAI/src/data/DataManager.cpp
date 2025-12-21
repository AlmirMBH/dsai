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

bool DataManager::loadMNIST(std::string imagePath, std::string labelPath, Dataset& dataset) {
    std::ifstream imageFile(imagePath, std::ios::binary);
    std::ifstream labelFile(labelPath, std::ios::binary);
    if (!imageFile || !labelFile) return false;
    
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

bool DataManager::loadImage(std::string path, Image& image) {
    int imageWidth, imageHeight, channelCount;
    unsigned char* imageData = stbi_load(path.c_str(), &imageWidth, &imageHeight, &channelCount, 1);
    if (!imageData) return false;
    
    std::vector<uint8_t> pixelData;
    for (int pixelIndex = 0; pixelIndex < imageWidth * imageHeight; ++pixelIndex) {
        pixelData.push_back(imageData[pixelIndex]);
    }
    image = Image(imageWidth, imageHeight, pixelData);
    stbi_image_free(imageData);
    return true;
}

bool DataManager::loadNumpy(std::string path, Dataset& dataset, int label, int maxSamples) {
    std::ifstream binaryFile(path, std::ios::binary);
    if (!binaryFile) return false;

    binaryFile.seekg(NUMPY_HEADER_SIZE);
    for (int sampleIndex = 0; sampleIndex < maxSamples; ++sampleIndex) {
        std::vector<double> featureValues;
        for (int pixelIndex = 0; pixelIndex < IMAGE_PIXELS; ++pixelIndex) {
            unsigned char pixelValue = 0;
            if (!binaryFile.read((char*)&pixelValue, 1)) break;
            featureValues.push_back(pixelValue / 255.0);
        }
        if (featureValues.size() < IMAGE_PIXELS) break;
        dataset.add(FeatureVector(featureValues), label);
    }
    return true;
}

void DataManager::loadShapes(Dataset& dataset, int samplesPerClass) {
    loadNumpy("../datasets/circle.npy", dataset, 0, samplesPerClass);
    loadNumpy("../datasets/square.npy", dataset, 1, samplesPerClass);
    loadNumpy("../datasets/triangle.npy", dataset, 2, samplesPerClass);
}

void DataManager::loadSymbols(Dataset& dataset, int samplesPerClass) {
    loadNumpy("../datasets/full_numpy_bitmap_star.npy", dataset, 0, samplesPerClass);
    loadNumpy("../datasets/full_numpy_bitmap_zigzag.npy", dataset, 1, samplesPerClass);
    loadNumpy("../datasets/full_numpy_bitmap_lightning.npy", dataset, 2, samplesPerClass);
}
