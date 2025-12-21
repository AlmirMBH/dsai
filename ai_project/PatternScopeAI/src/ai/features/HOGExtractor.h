#pragma once
#include "../../data/Image.h"
#include "../../data/FeatureVector.h"
#include <cmath>
#include <vector>

class HOGExtractor {
public:
    FeatureVector extract(const Image& image) {
        FeatureVector features(4); 
        std::vector<double> gradientBins(4, 0.0);
        
        for (int yCoordinate = 1; yCoordinate < image.getHeight() - 1; ++yCoordinate) {
            for (int xCoordinate = 1; xCoordinate < image.getWidth() - 1; ++xCoordinate) {
                double gradientX = image.getPixel(xCoordinate + 1, yCoordinate) - image.getPixel(xCoordinate - 1, yCoordinate);
                double gradientY = image.getPixel(xCoordinate, yCoordinate + 1) - image.getPixel(xCoordinate, yCoordinate - 1);
                double angle = std::atan2(gradientY, gradientX) * 180.0 / 3.14159;
                if (angle < 0) angle += 180.0;
                
                int binIndex = (int)(angle / 45.0) % 4;
                gradientBins[binIndex] += std::sqrt(gradientX * gradientX + gradientY * gradientY);
            }
        }
        
        for (int binIndex = 0; binIndex < 4; ++binIndex) features.set(binIndex, gradientBins[binIndex] / 1000.0);
        return features;
    }
};
