#include "StructuralFeatures.h"
#include <cmath>
#include <algorithm>

int StructuralFeatures::countEdges(const Image& image) {
    int edgeCount = 0;
    int width = image.getWidth();
    int height = image.getHeight();
    
    for (int y = 1; y < height - 1; ++y) {
        for (int x = 1; x < width - 1; ++x) {
            uint8_t center = image.getPixel(x, y);
            uint8_t right = image.getPixel(x + 1, y);
            uint8_t bottom = image.getPixel(x, y + 1);
            
            if (std::abs(static_cast<int>(center) - static_cast<int>(right)) > 30 ||
                std::abs(static_cast<int>(center) - static_cast<int>(bottom)) > 30) {
                edgeCount++;
            }
        }
    }
    
    return edgeCount;
}

int StructuralFeatures::countCorners(const Image& image) {
    int cornerCount = 0;
    int width = image.getWidth();
    int height = image.getHeight();
    
    for (int y = 1; y < height - 1; ++y) {
        for (int x = 1; x < width - 1; ++x) {
            uint8_t center = image.getPixel(x, y);
            uint8_t top = image.getPixel(x, y - 1);
            uint8_t bottom = image.getPixel(x, y + 1);
            uint8_t left = image.getPixel(x - 1, y);
            uint8_t right = image.getPixel(x + 1, y);
            
            int diff1 = std::abs(static_cast<int>(top) - static_cast<int>(center));
            int diff2 = std::abs(static_cast<int>(bottom) - static_cast<int>(center));
            int diff3 = std::abs(static_cast<int>(left) - static_cast<int>(center));
            int diff4 = std::abs(static_cast<int>(right) - static_cast<int>(center));
            
            if ((diff1 > 50 && diff3 > 50) || (diff2 > 50 && diff4 > 50) ||
                (diff1 > 50 && diff4 > 50) || (diff2 > 50 && diff3 > 50)) {
                cornerCount++;
            }
        }
    }
    
    return cornerCount;
}

double StructuralFeatures::getAspectRatio(const Image& image) {
    int width = image.getWidth();
    int height = image.getHeight();
    if (height > 0) {
        return static_cast<double>(width) / height;
    }
    return 1.0;
}

bool StructuralFeatures::hasSymmetry(const Image& image) {
    int width = image.getWidth();
    int height = image.getHeight();
    int matches = 0;
    int total = 0;
    
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width / 2; ++x) {
            uint8_t left = image.getPixel(x, y);
            uint8_t right = image.getPixel(width - 1 - x, y);
            if (std::abs(static_cast<int>(left) - static_cast<int>(right)) < 20) {
                matches++;
            }
            total++;
        }
    }
    
    return (total > 0) && (static_cast<double>(matches) / total > 0.7);
}

std::vector<double> StructuralFeatures::extractAll(const Image& image) {
    std::vector<double> features;
    features.push_back(static_cast<double>(countEdges(image)));
    features.push_back(static_cast<double>(countCorners(image)));
    features.push_back(getAspectRatio(image));
    features.push_back(hasSymmetry(image) ? 1.0 : 0.0);
    return features;
}

