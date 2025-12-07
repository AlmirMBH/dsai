#include "EdgeMapExtractor.h"
#include <cmath>
#include <algorithm>

EdgeMapExtractor::EdgeMapExtractor(int width, int height) 
    : targetWidth(width), targetHeight(height) {}

double EdgeMapExtractor::sobelX(const Image& image, int x, int y) {
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    double sum = 0.0;
    
    for (int i = -1; i <= 1; ++i) {
        for (int j = -1; j <= 1; ++j) {
            uint8_t pixel = image.getPixel(x + j, y + i);
            sum += gx[i + 1][j + 1] * static_cast<double>(pixel);
        }
    }
    
    return sum;
}

double EdgeMapExtractor::sobelY(const Image& image, int x, int y) {
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    double sum = 0.0;
    
    for (int i = -1; i <= 1; ++i) {
        for (int j = -1; j <= 1; ++j) {
            uint8_t pixel = image.getPixel(x + j, y + i);
            sum += gy[i + 1][j + 1] * static_cast<double>(pixel);
        }
    }
    
    return sum;
}

FeatureVector EdgeMapExtractor::extract(const Image& image) {
    int srcWidth = image.getWidth();
    int srcHeight = image.getHeight();
    
    std::vector<double> edgeMap(srcWidth * srcHeight, 0.0);
    double maxMagnitude = 0.0;
    
    for (int y = 1; y < srcHeight - 1; ++y) {
        for (int x = 1; x < srcWidth - 1; ++x) {
            double gx = sobelX(image, x, y);
            double gy = sobelY(image, x, y);
            double magnitude = std::sqrt(gx * gx + gy * gy);
            edgeMap[y * srcWidth + x] = magnitude;
            if (magnitude > maxMagnitude) {
                maxMagnitude = magnitude;
            }
        }
    }
    
    if (maxMagnitude > 0) {
        for (double& val : edgeMap) {
            val /= maxMagnitude;
        }
    }
    
    double scaleX = static_cast<double>(srcWidth) / targetWidth;
    double scaleY = static_cast<double>(srcHeight) / targetHeight;
    
    std::vector<double> features;
    features.reserve(targetWidth * targetHeight);
    
    for (int y = 0; y < targetHeight; ++y) {
        for (int x = 0; x < targetWidth; ++x) {
            int srcX = static_cast<int>(x * scaleX);
            int srcY = static_cast<int>(y * scaleY);
            features.push_back(edgeMap[srcY * srcWidth + srcX]);
        }
    }
    
    return FeatureVector(features);
}

