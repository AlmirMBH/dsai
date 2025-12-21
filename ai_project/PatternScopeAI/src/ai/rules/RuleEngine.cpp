#include "RuleEngine.h"
#include <cmath>
#include <algorithm>

RuleEngine::RuleEngine() {
    // Rule for digit 1 based on edge counts: few edges usually mean a simple shape like '1'.
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[0] < 30; }, 1, 0.6});
    // Rule for digit 8 based on edge counts: many edges indicate a complex shape like '8'.
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[0] > 120; }, 8, 0.7});
    // Rule for digit 1 based on aspect ratio: '1' is much taller than it is wide.
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[2] > 1.5; }, 1, 0.5});
    // Rule for digit 0 based on symmetry: '0' is highly symmetric from left to right.
    rules.push_back({[](const std::vector<double>& structuralFeatures) { return structuralFeatures[3] > 0.6; }, 0, 0.6});
}

/**
 * Count edges and corners in the image.
 * Calculate if the drawing is wide or tall and if it is 
 * symmetric. Return these four structural values.
 */
std::vector<double> RuleEngine::extractFeatures(const Image& image) {
    int edgeCount = 0;
    int cornerCount = 0;
    int imageWidth = image.getWidth();
    int imageHeight = image.getHeight();
    
    // Find the boundaries of the actual drawing to calculate aspect ratio correctly.
    int minX = imageWidth;
    int maxX = 0;
    int minY = imageHeight;
    int maxY = 0;
    bool hasDrawing = false;

    for (int yCoordinate = 1; yCoordinate < imageHeight - 1; ++yCoordinate) {
        for (int xCoordinate = 1; xCoordinate < imageWidth - 1; ++xCoordinate) {
            uint8_t pixel = image.getPixel(xCoordinate, yCoordinate);
            
            // Track boundaries of non-black pixels.
            if (pixel > 30) {
                if (xCoordinate < minX) { minX = xCoordinate; }
                if (xCoordinate > maxX) { maxX = xCoordinate; }
                if (yCoordinate < minY) { minY = yCoordinate; }
                if (yCoordinate > maxY) { maxY = yCoordinate; }
                hasDrawing = true;
            }

            bool isEdgeFound = false;
            // A change of brightness greater than 30 indicates an edge (outline) in the image.
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
            // If two pixels on opposite sides have a brightness difference of less than 20, 
            // they are considered symmetric.
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
        aspectRatio = contentHeight / contentWidth; // Height relative to Width
    }
    
    double symmetryScore = totalPixelsChecked > 0 ? (double)symmetryMatches / totalPixelsChecked : 0.0;
    
    return {(double)edgeCount, (double)cornerCount, aspectRatio, symmetryScore};
}

/**
 * Check the structural values against a set of 
 * predefined rules. Return a category if a rule matches.
 */
int RuleEngine::predict(const Image& image) {
    auto structuralFeatures = extractFeatures(image);
    for (auto& rule : rules) {
        if (rule.condition(structuralFeatures)) {
            return rule.label;
        }
    }
    return -1;
}

/**
 * Return a fixed certainty value if a rule matches.
 */
double RuleEngine::getConfidence(const Image& image) {
    auto structuralFeatures = extractFeatures(image);
    for (auto& rule : rules) {
        if (rule.condition(structuralFeatures)) {
            return rule.confidence;
        }
    }
    return 0.0;
}
