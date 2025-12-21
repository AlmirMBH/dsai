#include "PixelGridExtractor.h"

FeatureVector PixelGridExtractor::extract(const Image& image) {
    FeatureVector features;
    for (int yCoordinate = 0; yCoordinate < height; ++yCoordinate) {
        for (int xCoordinate = 0; xCoordinate < width; ++xCoordinate) {
            features.add(image.getPixel(xCoordinate, yCoordinate) / 255.0);
        }
    }
    return features;
}
