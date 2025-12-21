#include "RuleEngine.h"
#include <cmath>
#include <algorithm>

RuleEngine::RuleEngine() {
    // 1: Few edges, low complexity (often digit 1)
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[0] < 50 && structuralFeatures[1] < 10; }, 1, 0.6});
    // 8: Many edges, high complexity (often digit 8)
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[0] > 200 && structuralFeatures[1] > 30; }, 8, 0.7});
    // 1: Slim aspect ratio
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[2] > 1.2; }, 1, 0.5});
    // 0: High horizontal symmetry
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[3] > 0.5; }, 0, 0.6});
}

std::vector<double> RuleEngine::extractFeatures(const Image& image) {
    int edgeCount = 0;
    int cornerCount = 0;
    int imageWidth = image.getWidth();
    int imageHeight = image.getHeight();
    
    // Simple edge and corner detection
    for (int yCoordinate = 1; yCoordinate < imageHeight - 1; ++yCoordinate) {
        for (int xCoordinate = 1; xCoordinate < imageWidth - 1; ++xCoordinate) {
            bool isEdgeFound = false;
            if (std::abs(image.getPixel(xCoordinate, yCoordinate) - image.getPixel(xCoordinate + 1, yCoordinate)) > 30) {
                edgeCount++;
                isEdgeFound = true;
            }
            if (std::abs(image.getPixel(xCoordinate, yCoordinate) - image.getPixel(xCoordinate, yCoordinate + 1)) > 30) {
                edgeCount++;
                isEdgeFound = true;
            }
            
            if (isEdgeFound && std::abs(image.getPixel(xCoordinate, yCoordinate) - image.getPixel(xCoordinate + 1, yCoordinate + 1)) > 30) {
                cornerCount++;
            }
        }
    }
    
    int symmetryMatches = 0;
    int totalPixelsChecked = 0;
    for (int yCoordinate = 0; yCoordinate < imageHeight; ++yCoordinate) {
        for (int xCoordinate = 0; xCoordinate < imageWidth / 2; ++xCoordinate) {
            if (std::abs(image.getPixel(xCoordinate, yCoordinate) - image.getPixel(imageWidth - 1 - xCoordinate, yCoordinate)) < 20) symmetryMatches++;
            totalPixelsChecked++;
        }
    }
    
    double aspectRatio = imageHeight > 0 ? (double)imageWidth / imageHeight : 1.0;
    double symmetryScore = totalPixelsChecked > 0 ? (double)symmetryMatches / totalPixelsChecked : 0.0;
    
    return {(double)edgeCount, (double)cornerCount, aspectRatio, symmetryScore};
}

int RuleEngine::predict(const Image& image) {
    auto structuralFeatures = extractFeatures(image);
    for (auto& rule : rules) {
        if (rule.condition(structuralFeatures)) return rule.label;
    }
    return -1;
}

double RuleEngine::getConfidence(const Image& image) {
    auto structuralFeatures = extractFeatures(image);
    for (auto& rule : rules) {
        if (rule.condition(structuralFeatures)) return rule.confidence;
    }
    return 0.0;
}
