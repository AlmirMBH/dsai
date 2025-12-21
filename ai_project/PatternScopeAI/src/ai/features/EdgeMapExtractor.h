#pragma once
#include "../../data/Image.h"
#include "../../data/FeatureVector.h"
#include <cmath>

class EdgeMapExtractor {
public:
    /**
     * Count changes of light between pixels. Find edges. Return the density of edges.
     */
    FeatureVector extract(const Image& image) {
        FeatureVector features(2); 
        int horizontalEdgeCount = 0;
        int verticalEdgeCount = 0;
        
        for (int yCoordinate = 0; yCoordinate < image.getHeight(); ++yCoordinate) {
            for (int xCoordinate = 0; xCoordinate < image.getWidth(); ++xCoordinate) {
                if (xCoordinate < image.getWidth() - 1) {
                    // If the brightness difference between two side-by-side pixels is greater than 128 (half of 255), 
                    // we count it as a horizontal edge.
                    if (std::abs(image.getPixel(xCoordinate, yCoordinate) - image.getPixel(xCoordinate + 1, yCoordinate)) > 128) {
                        horizontalEdgeCount++;
                    }
                }
                if (yCoordinate < image.getHeight() - 1) {
                    // If the brightness difference between two top-and-bottom pixels is greater than 128, 
                    // we count it as a vertical edge.
                    if (std::abs(image.getPixel(xCoordinate, yCoordinate) - image.getPixel(xCoordinate, yCoordinate + 1)) > 128) {
                        verticalEdgeCount++;
                    }
                }
            }
        }
        // Return the average number of edges found per pixel in the image.
        features.set(0, (double)horizontalEdgeCount / (image.getWidth() * image.getHeight()));
        features.set(1, (double)verticalEdgeCount / (image.getWidth() * image.getHeight()));
        return features;
    }
};
