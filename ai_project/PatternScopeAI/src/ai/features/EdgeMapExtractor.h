#pragma once
#include "../../data/Image.h"
#include "../../data/FeatureVector.h"
#include <cmath>

class EdgeMapExtractor {
public:
    FeatureVector extract(const Image& image) {
        FeatureVector features(2); 
        int horizontalEdgeCount = 0;
        int verticalEdgeCount = 0;
        
        for (int yCoordinate = 0; yCoordinate < image.getHeight(); ++yCoordinate) {
            for (int xCoordinate = 0; xCoordinate < image.getWidth(); ++xCoordinate) {
                if (xCoordinate < image.getWidth() - 1) {
                    if (std::abs(image.getPixel(xCoordinate, yCoordinate) - image.getPixel(xCoordinate + 1, yCoordinate)) > 128) horizontalEdgeCount++;
                }
                if (yCoordinate < image.getHeight() - 1) {
                    if (std::abs(image.getPixel(xCoordinate, yCoordinate) - image.getPixel(xCoordinate, yCoordinate + 1)) > 128) verticalEdgeCount++;
                }
            }
        }
        features.set(0, (double)horizontalEdgeCount / (image.getWidth() * image.getHeight()));
        features.set(1, (double)verticalEdgeCount / (image.getWidth() * image.getHeight()));
        return features;
    }
};
