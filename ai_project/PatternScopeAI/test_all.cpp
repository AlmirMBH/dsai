#include <iostream>
#include <fstream>
#include "src/data/DataManager.h"
#include "src/ai/Engine.h"
#include "src/ai/features/EdgeMapExtractor.h"
#include "src/ai/features/HOGExtractor.h"

int main() {
    int passedTestsCount = 0;
    int totalTestsCount = 0;
    
    std::cout << "Starting PatternScope AI Backend Tests..." << std::endl;

    // Test 1: MNIST Loading
    totalTestsCount++;
    Dataset mnistDataset;
    if (DataManager::loadMNIST("../mnist/t10k-images.idx3-ubyte", "../mnist/t10k-labels.idx1-ubyte", mnistDataset)) {
        passedTestsCount++;
        std::cout << "✓ MNIST Loading Test passed" << std::endl;
    } else {
        std::cout << "✗ MNIST Loading Test failed" << std::endl;
    }

    // Test 2: Real Shape Loading
    totalTestsCount++;
    Dataset shapeDataset;
    DataManager::loadShapes(shapeDataset, 10);
    if (shapeDataset.size() > 0) {
        passedTestsCount++;
        std::cout << "✓ Real Shape Loading Test passed" << std::endl;
    } else {
        std::cout << "✗ Real Shape Loading Test failed" << std::endl;
    }

    // Test 3: Feature Extraction (EdgeMap)
    totalTestsCount++;
    EdgeMapExtractor edgeExtractor;
    Image testImage(28, 28);
    auto edgeFeatures = edgeExtractor.extract(testImage);
    if (edgeFeatures.size() == 2) {
        passedTestsCount++;
        std::cout << "✓ EdgeMap Extraction Test passed" << std::endl;
    } else {
        std::cout << "✗ EdgeMap Extraction Test failed" << std::endl;
    }

    // Test 4: Feature Extraction (HOG)
    totalTestsCount++;
    HOGExtractor hogExtractor;
    auto hogFeatures = hogExtractor.extract(testImage);
    if (hogFeatures.size() == 4) {
        passedTestsCount++;
        std::cout << "✓ HOG Extraction Test passed" << std::endl;
    } else {
        std::cout << "✗ HOG Extraction Test failed" << std::endl;
    }

    // Test 5: AI Engine Unified Prediction (Requires pre-trained models)
    totalTestsCount++;
    std::ifstream checkFile("models/shapes/knn.txt");
    if (!checkFile) {
        std::cout << "✗ AI Engine Prediction Test skipped (Model files not found. Run ./trainer first!)" << std::endl;
    } else {
        Engine recognitionEngine;
        auto result = recognitionEngine.predict(Mode::SHAPES, testImage);
        if (result.finalModelName != "") {
            passedTestsCount++;
            std::cout << "✓ AI Engine Prediction Test passed" << std::endl;
        } else {
            std::cout << "✗ AI Engine Prediction Test failed" << std::endl;
        }
    }

    std::cout << "------------------------------------------" << std::endl;
    std::cout << "Final Test Summary: " << passedTestsCount << "/" << totalTestsCount << " passed" << std::endl;
    std::cout << "------------------------------------------" << std::endl;
    
    return (passedTestsCount == totalTestsCount) ? 0 : 1;
}
