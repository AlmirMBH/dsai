#include "PixelGridExtractor.h"

/**
 * Take brightness of pixels. Convert pixels into a list of numbers. Return the list.
 */
FeatureVector PixelGridExtractor::extract(const Image& image) {
    FeatureVector features;
    for (int yCoordinate = 0; yCoordinate < height; ++yCoordinate) {
        for (int xCoordinate = 0; xCoordinate < width; ++xCoordinate) {
            // Divide by 255.0 to convert the brightness (0 to 255) into a scale between 0.0 and 1.0.
            // The models process numbers between 0 and 1 better than large whole numbers.
            features.add(image.getPixel(xCoordinate, yCoordinate) / 255.0);
        }
    }
    return features;
}
