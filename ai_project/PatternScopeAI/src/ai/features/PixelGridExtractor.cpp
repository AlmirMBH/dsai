#include "PixelGridExtractor.h"

PixelGridExtractor::PixelGridExtractor(int width, int height) 
    : targetWidth(width), targetHeight(height) {}

FeatureVector PixelGridExtractor::extract(const Image& image) {
    int srcWidth = image.getWidth();
    int srcHeight = image.getHeight();
    
    std::vector<double> features;
    features.reserve(targetWidth * targetHeight);
    
    double scaleX = static_cast<double>(srcWidth) / targetWidth;
    double scaleY = static_cast<double>(srcHeight) / targetHeight;
    
    for (int y = 0; y < targetHeight; ++y) {
        for (int x = 0; x < targetWidth; ++x) {
            int srcX = static_cast<int>(x * scaleX);
            int srcY = static_cast<int>(y * scaleY);
            uint8_t pixel = image.getPixel(srcX, srcY);
            features.push_back(static_cast<double>(pixel) / 255.0);
        }
    }
    
    return FeatureVector(features);
}

