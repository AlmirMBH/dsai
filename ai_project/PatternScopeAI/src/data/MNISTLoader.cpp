#include "MNISTLoader.h"
#include <fstream>
#include <cstdint>

static uint32_t readInt32(std::ifstream& file) {
    uint32_t value = 0;
    uint8_t bytes[4];
    file.read(reinterpret_cast<char*>(bytes), 4);
    value = (bytes[0] << 24) | (bytes[1] << 16) | (bytes[2] << 8) | bytes[3];
    return value;
}

bool MNISTLoader::loadImages(const std::string& imageFile, std::vector<Image>& images) {
    std::ifstream file(imageFile, std::ios::binary);
    if (!file.is_open()) {
        return false;
    }
    
    uint32_t magic = readInt32(file);
    if (magic != 2051) {
        file.close();
        return false;
    }
    
    uint32_t numImages = readInt32(file);
    uint32_t rows = readInt32(file);
    uint32_t cols = readInt32(file);
    
    images.clear();
    images.reserve(numImages);
    
    for (uint32_t i = 0; i < numImages; ++i) {
        std::vector<uint8_t> pixels(rows * cols);
        file.read(reinterpret_cast<char*>(pixels.data()), rows * cols);
        images.emplace_back(cols, rows, pixels);
    }
    
    file.close();
    return true;
}

bool MNISTLoader::loadLabels(const std::string& labelFile, std::vector<int>& labels) {
    std::ifstream file(labelFile, std::ios::binary);
    if (!file.is_open()) {
        return false;
    }
    
    uint32_t magic = readInt32(file);
    if (magic != 2049) {
        file.close();
        return false;
    }
    
    uint32_t numLabels = readInt32(file);
    
    labels.clear();
    labels.reserve(numLabels);
    
    for (uint32_t i = 0; i < numLabels; ++i) {
        uint8_t label;
        file.read(reinterpret_cast<char*>(&label), 1);
        labels.push_back(static_cast<int>(label));
    }
    
    file.close();
    return true;
}

bool MNISTLoader::loadDataset(const std::string& imageFile, const std::string& labelFile, Dataset& dataset) {
    std::vector<Image> images;
    std::vector<int> labels;
    
    if (!loadImages(imageFile, images) || !loadLabels(labelFile, labels)) {
        return false;
    }
    
    if (images.size() != labels.size()) {
        return false;
    }
    
    dataset.clear();
    for (size_t i = 0; i < images.size(); ++i) {
        std::vector<double> features;
        std::vector<uint8_t> data = images[i].getData();
        features.reserve(data.size());
        for (uint8_t pixel : data) {
            features.push_back(static_cast<double>(pixel) / 255.0);
        }
        dataset.add(FeatureVector(features), labels[i]);
    }
    
    return true;
}

