#pragma once
#include "../../data/Image.h"
#include "../../data/FeatureVector.h"

class PixelGridExtractor {
    int width, height;
public:
    PixelGridExtractor(int width = 28, int height = 28) : width(width), height(height) {}
    FeatureVector extract(const Image& image);
};
