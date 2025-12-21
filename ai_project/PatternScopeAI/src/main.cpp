#include <iostream>
#include <iomanip>
#include <algorithm>
#include "data/DataManager.h"
#include "ai/Engine.h"

int main(int argc, const char* argv[]) {
    Mode recognitionMode = Mode::DIGITS;
    
    if (argc > 1) { 
        std::string modeArgument = argv[1]; 
        if (modeArgument == "shapes") recognitionMode = Mode::SHAPES; 
        else if (modeArgument == "symbols") recognitionMode = Mode::SYMBOLS; 
    }
    
    Engine recognitionEngine; 
    Dataset testDataset;
    
    if (recognitionMode == Mode::DIGITS) {
        DataManager::loadMNIST("../mnist/t10k-images.idx3-ubyte", "../mnist/t10k-labels.idx1-ubyte", testDataset);
    } else if (recognitionMode == Mode::SHAPES) {
        DataManager::loadShapes(testDataset, 100);
    } else {
        DataManager::loadSymbols(testDataset, 100);
    }

    if (testDataset.size() == 0) {
        std::cout << "Error: Dataset could not be loaded." << std::endl;
        return 1;
    }
    
    int correctPredictionCount = 0;
    int samplesToTestCount = std::min((int)testDataset.size(), 100);
    
    std::cout << "Running recognition on " << samplesToTestCount << " samples..." << std::endl;
    
    for (int sampleIndex = 0; sampleIndex < samplesToTestCount; ++sampleIndex) {
        Image sampleImage(28, 28); 
        for (int pixelIndex = 0; pixelIndex < 784; ++pixelIndex) {
            sampleImage.setPixel(pixelIndex % 28, pixelIndex / 28, (uint8_t)(testDataset.getFeatures(sampleIndex).get(pixelIndex) * 255));
        }
        
        auto predictionResult = recognitionEngine.predict(recognitionMode, sampleImage);
        if (predictionResult.finalLabel == testDataset.getLabel(sampleIndex)) {
            correctPredictionCount++;
        }
        
        if (sampleIndex < 5) { // Show details for first 5
            std::string recognitionType = (recognitionMode == Mode::DIGITS) ? "number" : "pattern";
            std::cout << "Testing " << recognitionType << " " << testDataset.getLabel(sampleIndex) 
                      << " | True Label: " << testDataset.getLabel(sampleIndex) 
                      << " | Prediction: " << predictionResult.finalLabel 
                      << " | Confidence: " << std::fixed << std::setprecision(2) << predictionResult.finalConfidence 
                      << " | Model: " << predictionResult.finalModelName << std::endl;
            
            // Show model comparison
            std::cout << "   Comparison: ";
            for (auto const& modelResultEntry : predictionResult.modelComparison) {
                std::cout << modelResultEntry.first << "=" << modelResultEntry.second.label 
                          << " (" << std::fixed << std::setprecision(2) << modelResultEntry.second.confidence << ") | ";
            }
            std::cout << "\n";
        }
    }
    
    double overallAccuracy = (double)correctPredictionCount / samplesToTestCount;
    std::cout << "------------------------------------------" << std::endl;
    std::cout << "Overall Accuracy: " << std::fixed << std::setprecision(2) << (overallAccuracy * 100.0) << "%" << std::endl;
    std::cout << "------------------------------------------" << std::endl;
    
    return 0;
}
