#include "RuleEngine.h"
#include <cmath>
#include <algorithm>

RuleEngine::RuleEngine() {
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[0] < 30; }, 1, 0.6});
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[0] > 200; }, 8, 0.7});
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[2] > 1.5; }, 1, 0.5});
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[3] > 0.6; }, 0, 0.6});
}

std::vector<double> RuleEngine::extractFeatures(const Image& image) {
    int edgeCount = 0;
    int cornerCount = 0;
    int imageWidth = image.getWidth();
    int imageHeight = image.getHeight();
    
    int minX = imageWidth;
    int maxX = 0;
    int minY = imageHeight;
    int maxY = 0;
    bool hasDrawing = false;

    for (int yCoordinate = 1; yCoordinate < imageHeight - 1; ++yCoordinate) {
        for (int xCoordinate = 1; xCoordinate < imageWidth - 1; ++xCoordinate) {
            uint8_t pixel = image.getPixel(xCoordinate, yCoordinate);
            
            if (pixel > 30) {
                if (xCoordinate < minX) { minX = xCoordinate; }
                if (xCoordinate > maxX) { maxX = xCoordinate; }
                if (yCoordinate < minY) { minY = yCoordinate; }
                if (yCoordinate > maxY) { maxY = yCoordinate; }
                hasDrawing = true;
            }

            bool isEdgeFound = false;
            if (std::abs(pixel - image.getPixel(xCoordinate + 1, yCoordinate)) > 30) {
                edgeCount++;
                isEdgeFound = true;
            }
            if (std::abs(pixel - image.getPixel(xCoordinate, yCoordinate + 1)) > 30) {
                edgeCount++;
                isEdgeFound = true;
            }
            
            if (isEdgeFound && std::abs(pixel - image.getPixel(xCoordinate + 1, yCoordinate + 1)) > 30) {
                cornerCount++;
            }
        }
    }
    
    int symmetryMatches = 0;
    int totalPixelsChecked = 0;
    for (int yCoordinate = 0; yCoordinate < imageHeight; ++yCoordinate) {
        for (int xCoordinate = 0; xCoordinate < imageWidth / 2; ++xCoordinate) {
            if (std::abs(image.getPixel(xCoordinate, yCoordinate) - image.getPixel(imageWidth - 1 - xCoordinate, yCoordinate)) < 20) {
                symmetryMatches++;
            }
            totalPixelsChecked++;
        }
    }
    
    double aspectRatio = 1.0;
    if (hasDrawing) {
        double contentWidth = (maxX - minX) + 1.0;
        double contentHeight = (maxY - minY) + 1.0;
        aspectRatio = contentHeight / contentWidth;
    }
    
    double symmetryScore = totalPixelsChecked > 0 ? (double)symmetryMatches / totalPixelsChecked : 0.0;
    
    return {(double)edgeCount, (double)cornerCount, aspectRatio, symmetryScore};
}

int RuleEngine::predict(const Image& image) {
    auto structuralFeatures = extractFeatures(image);
    for (auto& rule : rules) {
        if (rule.condition(structuralFeatures)) {
            return rule.label;
        }
    }
    return -1;
}

double RuleEngine::getConfidence(const Image& image) {
    auto structuralFeatures = extractFeatures(image);
    for (auto& rule : rules) {
        if (rule.condition(structuralFeatures)) {
            return rule.confidence;
        }
    }
    return 0.0;
}
